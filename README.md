# OmniCache

**OmniCache (The "Gladiator" Cache)** is an O(1) cache eviction policy that aims to strictly isolate Recency from Frequency, achieving hit-rate parity with ARC (Adaptive Replacement Cache) while eliminating floating-point math and dynamic tier resizing.

![OmniCache vs ARC vs LRU](omnicache_benchmark.png)

## The Value Proposition

While standard caching algorithms like ARC and W-TinyLFU offer excellent scan resistance, they come with high implementation complexity:
* **ARC** requires four LRU queues, branching logic to balance them, and floating-point math to adapt its target parameter.
* **W-TinyLFU** requires a probabilistic Count-Min Sketch and a global decay loop that halves frequencies periodically.

**OmniCache provides ~99.9% of ARC's hit rate with a fraction of the complexity:**
* **Zero Math:** Uses static tier sizes (10% Window, 90% Main) and simple integer comparisons.
* **True O(1) Overhead:** No dynamic resizing or global loops. OmniCache executes up to 40% faster than ARC in software simulations due to fewer branch-prediction misses.
* **Strict Metadata Bounds:** Metadata memory is capped proportionally to capacity.

## The Algorithm ("Gladiator Combat")

OmniCache uses a 10% Window list and a 90% Protected Main list. When the Window is full, an item is evicted and challenges the oldest item in the Main list in a strict inequality competition: `if freq(challenger) > freq(defender)`.

If the challenger is from a sequential scan (freq = 1), it loses to the defender. The challenger is sent to the Ghost list, and the defender's frequency decays by 1. 

Once the oldest item in Main decays to a frequency of `1`, it acts as a permanent "Gladiator" at the gate: it will defeat an infinite number of incoming scan items (`1 > 1 == False`), perfectly freezing and protecting the hot data in the Main tier from being washed out by full-table scans. 

Because incoming hot data is accessed multiple times, it will achieve `freq >= 2` and successfully defeat the Gladiator to enter the Main tier, allowing the cache to adapt to new working sets.

## Running the Benchmarks

You can run the true benchmark and overhead tests yourself to verify the claims:

```bash
python real_benchmark.py
python overhead_test.py
```

## Usage

```python
from omnicache import OmniCache

# Initialize a cache with capacity 500
cache = OmniCache(500)

# Access keys
cache.access("user_123")
```

## License & Commercial Use
This project is licensed under the **GNU AGPLv3**. 
