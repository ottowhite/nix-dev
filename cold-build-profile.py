#!/usr/bin/env python3
"""Timed breakdown of a cold home-manager build.

Builds a homeConfiguration into a fresh, empty chroot store (so nothing already
in /nix/store counts as cached) with internal-json logging, timestamps each
activity event on receipt, and prints a phase breakdown (eval / download /
local-build) plus the slowest individual downloads and builds. The throwaway
store is removed on exit; your real store and active generation are untouched.

Usage:  ./cold-build-profile.py [config]      # default: ow20@server
Driven by `make -f Makefile.dev cold-build-breakdown [CONFIG=...]`.

Downloads and builds run concurrently, so summing per-item durations overcounts
wall time. Each phase figure is the UNION of its busy intervals (never exceeds
wall clock); the top-N lists show individual item durations for hotspots.
"""
import json, subprocess, sys, time, tempfile, os, re

CONFIG = sys.argv[1] if len(sys.argv) > 1 else "ow20@server"
FLAKE = os.path.dirname(os.path.abspath(__file__))

# ActivityType codes (nix src/libutil/include/nix/util/logging.hh)
store = tempfile.mkdtemp(prefix="coldprof.")
attr = f'{FLAKE}#homeConfigurations."{CONFIG}".activationPackage'
FEAT = ["--extra-experimental-features", "nix-command flakes"]

live = {}   # id -> (type, text, t_start)
done = {}   # type -> list of (t_start, t_stop, text)

# Phase 1 (eval): clear the flake eval cache and time a cold evaluation on its
# own. Eval interleaves with narinfo/substitution in the build stream and can't
# be carved out of it cleanly, so we measure it as a discrete step. This also
# warms the eval cache so phase 2's wall-clock is pure realization.
import shutil
shutil.rmtree(os.path.expanduser("~/.cache/nix/eval-cache-v6"), ignore_errors=True)
te0 = time.monotonic()
subprocess.run(["nix", "eval", "--raw", f"{attr}.drvPath", "--refresh", *FEAT],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
eval_t = time.monotonic() - te0

# Phase 2 (realize): build into the fresh store with a warm eval cache, so the
# internal-json activity stream is download + local-build only.
cmd = ["nix", "build", attr, "--store", store, "-v",
       "--log-format", "internal-json", *FEAT]

t0 = time.monotonic()
proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL,
                        bufsize=1, universal_newlines=True)
try:
    for line in proc.stderr:
        now = time.monotonic()
        if not line.startswith("@nix "):
            continue
        try:
            ev = json.loads(line[5:])
        except json.JSONDecodeError:
            continue
        act = ev.get("action")
        if act == "start":
            typ = ev.get("type", 0)
            live[ev["id"]] = (typ, ev.get("text", ""), now)
        elif act == "stop":
            rec = live.pop(ev.get("id"), None)
            if rec:
                typ, text, ts = rec
                done.setdefault(typ, []).append((ts, now, text))
finally:
    proc.wait()
t_end = time.monotonic()


def union(intervals):
    """Total wall-clock covered by the union of [start,stop) intervals."""
    if not intervals:
        return 0.0
    s = sorted((a, b) for a, b, _ in intervals)
    tot, cur_s, cur_e = 0.0, s[0][0], s[0][1]
    for a, b in s[1:]:
        if a > cur_e:
            tot += cur_e - cur_s
            cur_s, cur_e = a, b
        else:
            cur_e = max(cur_e, b)
    return tot + cur_e - cur_s


realize_wall = t_end - t0
wall = eval_t + realize_wall

copy_intervals = done.get(100, [])   # copyPath   = one substituted NAR each
xfer_intervals = done.get(101, [])   # fileTransfer = every HTTP GET (narinfo+nar)
dl_intervals = copy_intervals + xfer_intervals
build_intervals = done.get(105, [])  # local builds
qpi_intervals = done.get(109, [])    # narinfo path-info queries

dl_wall = union(dl_intervals)
build_wall = union(build_intervals)
qpi_wall = union(qpi_intervals)
both_wall = union(dl_intervals + build_intervals)
overlap = dl_wall + build_wall - both_wall


def topn(intervals, n=6):
    return sorted(((b - a, t) for a, b, t in intervals), reverse=True)[:n]


def short(text):
    m = re.search(r"/nix/store/[a-z0-9]+-([^'\s]+)", text)
    return m.group(1) if m else text[:60]


du = subprocess.run(["du", "-sh", store], capture_output=True, text=True).stdout.split()[0]

print("=" * 66)
print(f"COLD BUILD PROFILE  .#{CONFIG}")
print("=" * 66)
print(f"  wall clock total          {wall:7.1f}s   (100%)")
print(f"  |- eval (cold, discrete)  {eval_t:7.1f}s   ({eval_t/wall*100:4.1f}%)")
print(f"  |- realize (into store)   {realize_wall:7.1f}s   ({realize_wall/wall*100:4.1f}%)")
print(f"     within realize (phases run concurrently, so these overlap):")
print(f"     - narinfo queries      {qpi_wall:7.1f}s   {len(qpi_intervals)} lookups")
print(f"     - downloading (union)  {dl_wall:7.1f}s   {len(copy_intervals)} NARs, {len(xfer_intervals)} http GETs")
print(f"     - local builds (union) {build_wall:7.1f}s   {len(build_intervals)} drvs")
print(f"     - dl+build overlap     {overlap:7.1f}s")
print(f"  closure on disk           {du}")
print()
print("  slowest downloads (own duration; run in parallel):")
for d, t in topn(dl_intervals):
    print(f"    {d:6.1f}s  {short(t)}")
print()
print("  slowest local builds:")
for d, t in topn(build_intervals):
    print(f"    {d:6.1f}s  {short(t)}")

subprocess.run(f"chmod -R u+w {store} 2>/dev/null; rm -rf {store}", shell=True)
print(f"\n  (throwaway store {store} removed)")
