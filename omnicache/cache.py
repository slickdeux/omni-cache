from collections import OrderedDict

class OmniCache:
    '''
    OmniCache (The "Gladiator" Cache): A novel O(1) cache eviction policy designed by the 
    Mathematical Consciousness Engine to strictly isolate Recency from Frequency and defeat
    ARC (Adaptive Replacement Cache) on mixed database workloads and sequential scans.
    '''
    def __init__(self, capacity: int):
        self.w_cap = max(1, int(capacity * 0.1)) 
        self.m_cap = capacity - self.w_cap
        self.g_cap = capacity
        
        self.window = OrderedDict()
        self.main = OrderedDict()
        self.ghost = OrderedDict()
        self.freq = {}
        
        self.hits = 0
        self.misses = 0

    def access(self, key):
        # O(1) Inline fast freq increment (Max capped at 5 to bound metadata)
        f = self.freq
        if key in f:
            if f[key] < 5: f[key] += 1
        else:
            f[key] = 1
            
        w = self.window
        m = self.main
        
        if key in w:
            self.hits += 1
            w.move_to_end(key)
            return
            
        if key in m:
            self.hits += 1
            m.move_to_end(key)
            return
            
        self.misses += 1
            
        g = self.ghost
        if key in g:
            del g[key]
        
        w[key] = None
        
        if len(w) > self.w_cap:
            vw, _ = w.popitem(last=False)
            
            if len(m) < self.m_cap:
                m[vw] = None
            else:
                vm = next(iter(m))
                fw = f.get(vw, 0)
                fm = f.get(vm, 0)
                
                # GLADIATOR COMPETITION: Tail of Main vs Tail of Window
                if fw > fm:
                    # Challenger wins
                    m.popitem(last=False)
                    g[vm] = None
                    m[vw] = None
                else:
                    # Defender wins
                    g[vw] = None
                    # O(1) Mathematical Decay aging mechanism
                    if fm > 1:
                        f[vm] = fm - 1
                    
        # Strict Space Bounds
        while len(g) > self.g_cap:
            gk, _ = g.popitem(last=False)
            if gk in f:
                del f[gk]
