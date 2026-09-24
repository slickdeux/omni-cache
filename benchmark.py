import random
import time
from benchmark import ARCCache, LRUCache, generate_zipf_trace
from omnicache.cache import OmniCache

def generate_true_scan_trace(num_items, start_index=0):
    """
    Generates a true sequential scan over completely unique items.
    Unlike the original benchmark, this does NOT loop over the same elements,
    representing a real full-table scan or database backup.
    """
    return list(range(start_index, start_index + num_items))

def run_benchmark(name, trace, capacity):
    print(f"\n=== Benchmark: {name} | Trace size: {len(trace)} | Cache capacity: {capacity} ===")
    
    # LRU
    lru = LRUCache(capacity)
    for key in trace: lru.access(key)
    lru_hit_rate = (lru.hits / len(trace)) * 100

    # ARC
    arc = ARCCache(capacity)
    for key in trace: arc.access(key)
    arc_hit_rate = (arc.hits / len(trace)) * 100

    # OmniCache
    omni = OmniCache(capacity)
    for key in trace: omni.access(key)
    omni_hit_rate = (omni.hits / len(trace)) * 100

    print(f"LRU  Hit Rate: {lru_hit_rate:.2f}%")
    print(f"ARC  Hit Rate: {arc_hit_rate:.2f}%")
    print(f"Omni Hit Rate: {omni_hit_rate:.2f}%")

if __name__ == "__main__":
    print("Generating Traces... (this might take a few seconds)")
    capacity = 500
    random.seed(42)
    
    # 1. Zipfian Trace (Simulates a standard database workload where some keys are hot)
    zipf_trace = generate_zipf_trace(num_items=5000, num_requests=20000, alpha=1.2)
    run_benchmark("Zipfian Database Workload", zipf_trace, capacity)

    # 2. True Sequential Scan
    # A true scan of 6000 completely unique items. 
    # This exposes the 15% hit rate trick - on a real scan, it should be 0%.
    true_scan_trace = generate_true_scan_trace(6000, start_index=10000)
    run_benchmark("True Sequential Scan (6000 unique items)", true_scan_trace, capacity)
    
    # 3. Mixed Workload (Zipfian mixed with a TRUE scan)
    # This tests the ACTUAL benefit of scan resistance: preserving the hot data
    # that was established before the scan occurred, so it's still there when 
    # the normal workload resumes.
    mixed_trace = zipf_trace[:10000] + true_scan_trace + zipf_trace[10000:]
    run_benchmark("Mixed Workload (DB -> True Scan -> DB)", mixed_trace, capacity)
