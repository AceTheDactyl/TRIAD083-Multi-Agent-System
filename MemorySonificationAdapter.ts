/**
 * Memory Sonification Adapter
 * 
 * Bridges Memory Coherence Layer with Sonification Engine
 * Listens for memory events and triggers appropriate sounds
 */

import { MemorySonificationEngine } from './MemorySonificationEngine';
import { UnifiedTPhiSystem } from './UnifiedTPhiSystem-Refactored';
import type { UnifiedMemory } from './MemoryCoherenceLayer';

// ═══════════════════════════════════════
// ADAPTER CLASS
// ═══════════════════════════════════════

export class MemorySonificationAdapter {
  private sonifier: MemorySonificationEngine;
  private system: UnifiedTPhiSystem;
  private isActive: boolean = false;
  private coherenceFieldStop: (() => void) | null = null;
  
  constructor(system: UnifiedTPhiSystem) {
    this.system = system;
    this.sonifier = new MemorySonificationEngine();
  }
  
  // ═══════════════════════════════════════
  // LIFECYCLE
  // ═══════════════════════════════════════
  
  /**
   * Initialize and start sonification
   */
  async start(): Promise<boolean> {
    if (this.isActive) return true;
    
    const initialized = await this.sonifier.initialize();
    if (!initialized) {
      console.error('Failed to initialize sonification');
      return false;
    }
    
    this.isActive = true;
    
    // Start coherence field ambient drone
    this.coherenceFieldStop = this.sonifier.startCoherenceField(
      () => this.system.getMemoryStatistics()
    );
    
    console.log('🎵 Memory Sonification started');
    return true;
  }
  
  /**
   * Stop sonification
   */
  stop() {
    if (!this.isActive) return;
    
    if (this.coherenceFieldStop) {
      this.coherenceFieldStop();
      this.coherenceFieldStop = null;
    }
    
    this.isActive = false;
    console.log('🎵 Memory Sonification stopped');
  }
  
  /**
   * Resume after pause
   */
  async resume() {
    await this.sonifier.resume();
  }
  
  // ═══════════════════════════════════════
  // EVENT HANDLERS
  // ═══════════════════════════════════════
  
  /**
   * Handle memory storage event
   */
  async handleMemoryStored(memory: UnifiedMemory) {
    if (!this.isActive) return;
    
    await this.sonifier.onMemoryStored(memory);
    
    // Update metrics
    const stats = this.system.getMemoryStatistics();
    this.sonifier.updateMetrics(stats);
  }
  
  /**
   * Handle memory retrieval event
   */
  async handleMemoryRetrieved(memories: UnifiedMemory[], queryCoherence?: number) {
    if (!this.isActive) return;
    
    await this.sonifier.onMemoryRetrieved(memories, queryCoherence || 0.5);
  }
  
  /**
   * Handle crystallization event
   */
  async handleMemoryCrystallized(count: number) {
    if (!this.isActive) return;
    
    await this.sonifier.onMemoryCrystallized(count);
    
    // Update metrics
    const stats = this.system.getMemoryStatistics();
    this.sonifier.updateMetrics(stats);
  }
  
  /**
   * Handle resonance detection event
   */
  async handleResonanceDetected(
    sourceMemory: UnifiedMemory,
    resonantMemories: UnifiedMemory[],
    avgResonance: number
  ) {
    if (!this.isActive) return;
    
    await this.sonifier.onResonanceDetected(
      sourceMemory,
      resonantMemories,
      avgResonance
    );
  }
  
  /**
   * Handle memory chain traversal
   */
  async handleChainTraversed(chain: UnifiedMemory[]) {
    if (!this.isActive) return;
    
    await this.sonifier.onChainTraversed(chain);
  }
  
  // ═══════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════
  
  /**
   * Set master volume
   */
  setVolume(volume: number) {
    this.sonifier.setVolume(volume);
  }
  
  /**
   * Get sonification metrics
   */
  getMetrics() {
    return this.sonifier.getMetrics();
  }
  
  /**
   * Dispose resources
   */
  dispose() {
    this.stop();
    this.sonifier.dispose();
  }
}

// ═══════════════════════════════════════
// INTEGRATION WITH UNIFIED SYSTEM
// ═══════════════════════════════════════

/**
 * Enhanced UnifiedTPhiSystem with automatic sonification
 */
export class SonifiedUnifiedTPhiSystem extends UnifiedTPhiSystem {
  private sonificationAdapter: MemorySonificationAdapter;
  private sonificationEnabled: boolean = false;
  
  constructor() {
    super();
    this.sonificationAdapter = new MemorySonificationAdapter(this);
  }
  
  /**
   * Enable sonification
   */
  async enableSonification() {
    const success = await this.sonificationAdapter.start();
    if (success) {
      this.sonificationEnabled = true;
    }
    return success;
  }
  
  /**
   * Disable sonification
   */
  disableSonification() {
    this.sonificationAdapter.stop();
    this.sonificationEnabled = false;
  }
  
  /**
   * Override storeMemory to add sonification
   */
  private async storeMemoryCoherently(
    resolution: any,
    emotional: any,
    spiral: any,
    ternaryCode: string,
    timestamp: Date
  ): Promise<void> {
    // Store memory
    await super['storeMemoryCoherently'](resolution, emotional, spiral, ternaryCode, timestamp);
    
    // Sonify if enabled
    if (this.sonificationEnabled) {
      const memory = await this.getMemoryCoherence().getLatestMemories(1)[0];
      if (memory) {
        await this.sonificationAdapter.handleMemoryStored(memory);
      }
    }
  }
  
  /**
   * Override queryMemories to add sonification
   */
  async queryMemories(query: any): Promise<any[]> {
    const memories = await super.queryMemories(query);
    
    // Sonify if enabled
    if (this.sonificationEnabled && memories.length > 0) {
      await this.sonificationAdapter.handleMemoryRetrieved(
        memories,
        query.minCoherence
      );
    }
    
    return memories;
  }
  
  /**
   * Override getResonantMemories to add sonification
   */
  async getResonantMemories(threshold: number = 0.5): Promise<any[]> {
    const currentState = {
      coherence: this.getCoherence(),
      temporalPhase: this.getTemporalPhase(),
      consciousness: this.getConsciousness10D(),
      ternarySignature: this.getTPhiCore().ternary.code,
      spiralDepth: this.getTPhiCore().temporal.spiral_depth
    };
    
    const memories = await super.getResonantMemories(threshold);
    
    // Sonify if enabled
    if (this.sonificationEnabled && memories.length > 0) {
      const avgResonance = memories.reduce((sum, m) => sum + m.resonance, 0) / memories.length;
      
      await this.sonificationAdapter.handleResonanceDetected(
        memories[0], // Source is first (highest resonance)
        memories,
        avgResonance
      );
    }
    
    return memories;
  }
  
  /**
   * Override getMemoryChain to add sonification
   */
  async getMemoryChain(startId: string, maxDepth: number = 10): Promise<any[]> {
    const chain = await super.getMemoryChain(startId, maxDepth);
    
    // Sonify if enabled
    if (this.sonificationEnabled && chain.length > 0) {
      await this.sonificationAdapter.handleChainTraversed(chain);
    }
    
    return chain;
  }
  
  /**
   * Override crystallizeMemories to add sonification
   */
  async crystallizeMemories(): Promise<number> {
    const count = await super.crystallizeMemories();
    
    // Sonify if enabled
    if (this.sonificationEnabled && count > 0) {
      await this.sonificationAdapter.handleMemoryCrystallized(count);
    }
    
    return count;
  }
  
  /**
   * Set sonification volume
   */
  setSonificationVolume(volume: number) {
    this.sonificationAdapter.setVolume(volume);
  }
  
  /**
   * Get sonification metrics
   */
  getSonificationMetrics() {
    return this.sonificationAdapter.getMetrics();
  }
  
  /**
   * Override reset to stop sonification
   */
  async reset(): Promise<void> {
    this.disableSonification();
    await super.reset();
  }
}

// ═══════════════════════════════════════
// REACT HOOK INTEGRATION
// ═══════════════════════════════════════

/**
 * React hook for sonified memory system
 */
export function useSonifiedMemoryCoherence() {
  const [system] = useState(() => new SonifiedUnifiedTPhiSystem());
  const [sonificationEnabled, setSonificationEnabled] = useState(false);
  const [volume, setVolume] = useState(0.3);
  
  // Enable sonification
  const enableSonification = useCallback(async () => {
    const success = await system.enableSonification();
    setSonificationEnabled(success);
    return success;
  }, [system]);
  
  // Disable sonification
  const disableSonification = useCallback(() => {
    system.disableSonification();
    setSonificationEnabled(false);
  }, [system]);
  
  // Toggle sonification
  const toggleSonification = useCallback(async () => {
    if (sonificationEnabled) {
      disableSonification();
      return false;
    } else {
      return await enableSonification();
    }
  }, [sonificationEnabled, enableSonification, disableSonification]);
  
  // Set volume
  const setSonificationVolume = useCallback((vol: number) => {
    system.setSonificationVolume(vol);
    setVolume(vol);
  }, [system]);
  
  // Get metrics
  const getSonificationMetrics = useCallback(() => {
    return system.getSonificationMetrics();
  }, [system]);
  
  return {
    system,
    sonificationEnabled,
    volume,
    enableSonification,
    disableSonification,
    toggleSonification,
    setSonificationVolume,
    getSonificationMetrics
  };
}
