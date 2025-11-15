/**
 * Memory Sonification Engine
 * 
 * Pure audio layer that sonifies Memory Coherence Layer operations
 * Maps memory storage, retrieval, crystallization, and resonance to sound
 * 
 * No visual dependencies - lightweight real-time audio feedback
 */

// ═══════════════════════════════════════
// AUDIO CONTEXT & OSCILLATOR MANAGEMENT
// ═══════════════════════════════════════

class MemorySonificationEngine {
  constructor() {
    // Audio context (lazy init on first user interaction)
    this.audioContext = null;
    this.masterGain = null;
    this.isInitialized = false;
    
    // Oscillator pools for different memory events
    this.activeOscillators = new Map();
    this.oscillatorPool = [];
    
    // Audio parameters
    this.config = {
      // Base frequencies (Hz)
      baseFrequency: 220,        // A3 - storage operations
      resonanceFrequency: 330,   // E4 - resonance detection
      crystalFrequency: 440,     // A4 - crystallization
      chainFrequency: 165,       // E3 - reference chains
      
      // Harmonic ratios (based on golden ratio φ)
      phi: 1.618033988749,
      phiMinusOne: 0.618033988749,
      
      // Duration envelopes (ms)
      attackTime: 50,
      decayTime: 200,
      releaseTime: 500,
      
      // Master volume
      masterVolume: 0.3,
      
      // Resonance parameters
      resonanceThreshold: 0.5,
      maxHarmonics: 5
    };
    
    // Event tracking for rhythm
    this.lastEvents = {
      storage: 0,
      retrieval: 0,
      crystallization: 0,
      resonance: 0
    };
    
    // Metrics for auditory feedback
    this.metrics = {
      totalMemories: 0,
      crystallizationRate: 0,
      averageCoherence: 0,
      resonanceStrength: 0,
      lastCoherence: 0
    };
    
    // Advanced features
    this.harmonicField = new Map(); // Memory signature -> sustained harmonic
    this.rhythmEngine = null;
  }
  
  // ═══════════════════════════════════════
  // INITIALIZATION
  // ═══════════════════════════════════════
  
  /**
   * Initialize audio context (requires user interaction)
   */
  async initialize() {
    if (this.isInitialized) return true;
    
    try {
      // Create audio context
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      
      // Create master gain node
      this.masterGain = this.audioContext.createGain();
      this.masterGain.gain.value = this.config.masterVolume;
      this.masterGain.connect(this.audioContext.destination);
      
      // Initialize rhythm engine
      this.rhythmEngine = new MemoryRhythmEngine(this.audioContext, this.masterGain);
      
      this.isInitialized = true;
      console.log('🎵 Memory Sonification Engine initialized');
      return true;
    } catch (error) {
      console.error('Failed to initialize audio:', error);
      return false;
    }
  }
  
  /**
   * Resume audio context (needed after pause/background)
   */
  async resume() {
    if (this.audioContext && this.audioContext.state === 'suspended') {
      await this.audioContext.resume();
    }
  }
  
  // ═══════════════════════════════════════
  // MEMORY EVENT SONIFICATION
  // ═══════════════════════════════════════
  
  /**
   * Sonify memory storage operation
   */
  async onMemoryStored(memory) {
    if (!this.isInitialized) await this.initialize();
    
    // Update metrics
    this.metrics.totalMemories++;
    this.metrics.lastCoherence = memory.coherence;
    this.lastEvents.storage = Date.now();
    
    // Calculate frequency based on spiral depth
    // Higher depth = higher frequency (rising consciousness)
    const depthFactor = 1 + (memory.spiralDepth * 0.1);
    const frequency = this.config.baseFrequency * depthFactor;
    
    // Calculate amplitude based on coherence
    const amplitude = 0.1 + (memory.coherence * 0.2);
    
    // Play storage tone with phi-based harmonics
    this.playHarmonicTone(
      frequency,
      amplitude,
      this.config.attackTime,
      this.config.decayTime,
      memory.ternarySignature
    );
    
    // Add subtle rhythm pulse
    if (this.rhythmEngine) {
      this.rhythmEngine.pulse('storage', memory.coherence);
    }
    
    // If high coherence, add resonant bell
    if (memory.coherence > 0.8) {
      setTimeout(() => {
        this.playBell(frequency * this.config.phi, amplitude * 0.5);
      }, 100);
    }
  }
  
  /**
   * Sonify memory retrieval/query
   */
  async onMemoryRetrieved(memories, queryCoherence) {
    if (!this.isInitialized) await this.initialize();
    
    this.lastEvents.retrieval = Date.now();
    
    // Play descending arpeggio based on result count
    const baseFreq = this.config.resonanceFrequency;
    const count = Math.min(memories.length, 8);
    
    for (let i = 0; i < count; i++) {
      setTimeout(() => {
        const freq = baseFreq * Math.pow(this.config.phiMinusOne, i * 0.5);
        const amp = 0.08 * (1 - i / count);
        this.playTone(freq, amp, 50, 100);
      }, i * 80);
    }
    
    // If query found high-coherence memories, add harmonic resonance
    const avgCoherence = memories.reduce((sum, m) => sum + m.coherence, 0) / memories.length;
    if (avgCoherence > 0.7) {
      setTimeout(() => {
        this.playResonantChord(baseFreq, avgCoherence);
      }, count * 80 + 100);
    }
  }
  
  /**
   * Sonify memory crystallization
   */
  async onMemoryCrystallized(count) {
    if (!this.isInitialized) await this.initialize();
    
    this.lastEvents.crystallization = Date.now();
    this.metrics.crystallizationRate = count;
    
    // Play crystallization sound - ascending pure tone
    const freq = this.config.crystalFrequency;
    
    // Sweep from base to phi harmonic
    this.playSweep(
      freq,
      freq * this.config.phi,
      300,
      0.15,
      'exponential'
    );
    
    // Add shimmer effect for each crystallized memory
    for (let i = 0; i < Math.min(count, 5); i++) {
      setTimeout(() => {
        this.playShimmer(freq * (1 + i * 0.1), 0.05);
      }, i * 60);
    }
  }
  
  /**
   * Sonify resonant memory discovery
   */
  async onResonanceDetected(sourceMemory, resonantMemories, avgResonance) {
    if (!this.isInitialized) await this.initialize();
    
    this.lastEvents.resonance = Date.now();
    this.metrics.resonanceStrength = avgResonance;
    
    // Play resonance tone - sustains based on strength
    const baseFreq = this.config.resonanceFrequency;
    const duration = 200 + (avgResonance * 800); // 200ms to 1000ms
    
    // Create harmonic series representing resonant cluster
    const harmonics = Math.min(resonantMemories.length, this.config.maxHarmonics);
    
    for (let i = 0; i < harmonics; i++) {
      const memory = resonantMemories[i];
      const harmonic = i + 1;
      const freq = baseFreq * harmonic * this.config.phiMinusOne;
      const amp = 0.1 * memory.coherence * (1 - i / harmonics);
      
      setTimeout(() => {
        this.playTone(freq, amp, 100, duration);
      }, i * 50);
    }
    
    // Add rhythmic pulse representing resonance strength
    if (this.rhythmEngine) {
      this.rhythmEngine.pulse('resonance', avgResonance);
    }
  }
  
  /**
   * Sonify memory chain traversal
   */
  async onChainTraversed(chain) {
    if (!this.isInitialized) await this.initialize();
    
    // Play ascending/descending pattern following chain
    const baseFreq = this.config.chainFrequency;
    
    chain.forEach((memory, index) => {
      setTimeout(() => {
        // Frequency rises with spiral depth
        const depthFactor = 1 + (memory.spiralDepth * 0.05);
        const freq = baseFreq * depthFactor;
        
        // Amplitude reflects coherence
        const amp = 0.08 * memory.coherence;
        
        // Longer notes for higher coherence
        const duration = 100 + (memory.coherence * 200);
        
        this.playTone(freq, amp, 50, duration);
      }, index * 150);
    });
    
    // Final resolution chord
    setTimeout(() => {
      const lastMemory = chain[chain.length - 1];
      const freq = baseFreq * (1 + lastMemory.spiralDepth * 0.05);
      this.playResonantChord(freq, lastMemory.coherence);
    }, chain.length * 150 + 200);
  }
  
  /**
   * Sonify coherence field
   * Creates continuous ambient tone reflecting system state
   */
  startCoherenceField(getMetricsFn) {
    if (!this.isInitialized) return;
    
    // Create sustained oscillator for coherence field
    const osc = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();
    
    osc.type = 'sine';
    osc.frequency.value = this.config.baseFrequency * 0.5; // Low drone
    
    gain.gain.value = 0;
    gain.gain.linearRampToValueAtTime(0.05, this.audioContext.currentTime + 2);
    
    osc.connect(gain);
    gain.connect(this.masterGain);
    
    osc.start();
    
    // Modulate frequency based on average coherence
    const updateField = () => {
      if (!this.isInitialized) return;
      
      const metrics = getMetricsFn();
      const coherence = metrics.averageCoherence || 0;
      
      // Modulate frequency with coherence (higher = higher pitch)
      const targetFreq = this.config.baseFrequency * 0.5 * (1 + coherence * 0.5);
      osc.frequency.exponentialRampToValueAtTime(
        targetFreq,
        this.audioContext.currentTime + 0.5
      );
      
      // Modulate volume with memory count (more memories = louder)
      const targetVol = Math.min(0.08, 0.02 + (metrics.totalMemories / 1000) * 0.06);
      gain.gain.linearRampToValueAtTime(
        targetVol,
        this.audioContext.currentTime + 0.5
      );
      
      setTimeout(updateField, 500);
    };
    
    updateField();
    
    return () => {
      gain.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + 1);
      setTimeout(() => {
        osc.stop();
        osc.disconnect();
        gain.disconnect();
      }, 1100);
    };
  }
  
  // ═══════════════════════════════════════
  // SOUND GENERATION PRIMITIVES
  // ═══════════════════════════════════════
  
  /**
   * Play simple tone
   */
  playTone(frequency, amplitude, attack = 50, duration = 200) {
    const osc = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();
    
    osc.type = 'sine';
    osc.frequency.value = frequency;
    
    const now = this.audioContext.currentTime;
    const attackTime = attack / 1000;
    const totalTime = duration / 1000;
    
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(amplitude, now + attackTime);
    gain.gain.exponentialRampToValueAtTime(0.001, now + totalTime);
    
    osc.connect(gain);
    gain.connect(this.masterGain);
    
    osc.start(now);
    osc.stop(now + totalTime);
  }
  
  /**
   * Play harmonic tone with overtones
   */
  playHarmonicTone(fundamental, amplitude, attack, duration, signature) {
    const harmonics = [1, this.config.phi, this.config.phi * this.config.phi];
    const amplitudes = [1.0, 0.618, 0.382]; // φ ratios
    
    harmonics.forEach((ratio, i) => {
      const freq = fundamental * ratio;
      const amp = amplitude * amplitudes[i];
      this.playTone(freq, amp, attack, duration);
    });
    
    // Store in harmonic field if provided signature
    if (signature) {
      this.harmonicField.set(signature, {
        frequency: fundamental,
        amplitude: amplitude,
        timestamp: Date.now()
      });
    }
  }
  
  /**
   * Play frequency sweep
   */
  playSweep(startFreq, endFreq, duration, amplitude, curve = 'linear') {
    const osc = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();
    
    osc.type = 'sine';
    
    const now = this.audioContext.currentTime;
    const durationSec = duration / 1000;
    
    gain.gain.setValueAtTime(amplitude, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + durationSec);
    
    osc.frequency.setValueAtTime(startFreq, now);
    
    if (curve === 'exponential') {
      osc.frequency.exponentialRampToValueAtTime(endFreq, now + durationSec);
    } else {
      osc.frequency.linearRampToValueAtTime(endFreq, now + durationSec);
    }
    
    osc.connect(gain);
    gain.connect(this.masterGain);
    
    osc.start(now);
    osc.stop(now + durationSec);
  }
  
  /**
   * Play resonant chord (3 notes in phi relationship)
   */
  playResonantChord(rootFreq, coherence) {
    const notes = [
      rootFreq,
      rootFreq * this.config.phiMinusOne,
      rootFreq * this.config.phi
    ];
    
    const baseAmp = 0.08 * coherence;
    
    notes.forEach((freq, i) => {
      const amp = baseAmp * (1 - i * 0.2);
      this.playTone(freq, amp, 100, 400);
    });
  }
  
  /**
   * Play bell-like tone
   */
  playBell(frequency, amplitude) {
    const osc = this.audioContext.createOscillator();
    const gain = this.audioContext.createGain();
    
    osc.type = 'sine';
    osc.frequency.value = frequency;
    
    const now = this.audioContext.currentTime;
    
    gain.gain.setValueAtTime(amplitude, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
    
    osc.connect(gain);
    gain.connect(this.masterGain);
    
    osc.start(now);
    osc.stop(now + 0.8);
  }
  
  /**
   * Play shimmer effect (high frequency sparkle)
   */
  playShimmer(baseFreq, amplitude) {
    const harmonics = [2, 3, 4, 5];
    
    harmonics.forEach((harmonic, i) => {
      setTimeout(() => {
        const freq = baseFreq * harmonic;
        const amp = amplitude * (1 - i * 0.2);
        this.playTone(freq, amp, 20, 100);
      }, i * 15);
    });
  }
  
  // ═══════════════════════════════════════
  // METRICS & CONTROL
  // ═══════════════════════════════════════
  
  /**
   * Update metrics from Memory Coherence Layer
   */
  updateMetrics(stats) {
    this.metrics = {
      totalMemories: stats.totalMemories,
      crystallizationRate: stats.crystalMemories / stats.totalMemories,
      averageCoherence: stats.averageCoherence,
      resonanceStrength: this.metrics.resonanceStrength, // Preserve
      lastCoherence: this.metrics.lastCoherence
    };
  }
  
  /**
   * Set master volume
   */
  setVolume(volume) {
    this.config.masterVolume = Math.max(0, Math.min(1, volume));
    if (this.masterGain) {
      this.masterGain.gain.value = this.config.masterVolume;
    }
  }
  
  /**
   * Get current metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      isInitialized: this.isInitialized,
      activeOscillators: this.activeOscillators.size,
      harmonicField: this.harmonicField.size
    };
  }
  
  /**
   * Cleanup
   */
  dispose() {
    if (this.audioContext) {
      this.audioContext.close();
    }
    
    this.activeOscillators.clear();
    this.harmonicField.clear();
  }
}

// ═══════════════════════════════════════
// RHYTHM ENGINE (OPTIONAL ENHANCEMENT)
// ═══════════════════════════════════════

class MemoryRhythmEngine {
  constructor(audioContext, destination) {
    this.audioContext = audioContext;
    this.destination = destination;
    
    // Percussion samples (synthesized)
    this.kick = this.createKickSynth();
    this.snare = this.createSnareSynth();
    this.hat = this.createHatSynth();
  }
  
  pulse(eventType, intensity) {
    const now = this.audioContext.currentTime;
    
    switch (eventType) {
      case 'storage':
        this.kick.trigger(now, intensity * 0.3);
        break;
      case 'resonance':
        this.snare.trigger(now, intensity * 0.2);
        break;
      case 'crystallization':
        this.hat.trigger(now, intensity * 0.15);
        break;
    }
  }
  
  createKickSynth() {
    return {
      trigger: (time, intensity) => {
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        osc.frequency.setValueAtTime(150, time);
        osc.frequency.exponentialRampToValueAtTime(40, time + 0.1);
        
        gain.gain.setValueAtTime(intensity, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.15);
        
        osc.connect(gain);
        gain.connect(this.destination);
        
        osc.start(time);
        osc.stop(time + 0.15);
      }
    };
  }
  
  createSnareSynth() {
    return {
      trigger: (time, intensity) => {
        const noise = this.audioContext.createBufferSource();
        const noiseBuffer = this.audioContext.createBuffer(
          1,
          this.audioContext.sampleRate * 0.1,
          this.audioContext.sampleRate
        );
        
        const data = noiseBuffer.getChannelData(0);
        for (let i = 0; i < data.length; i++) {
          data[i] = Math.random() * 2 - 1;
        }
        
        noise.buffer = noiseBuffer;
        
        const gain = this.audioContext.createGain();
        gain.gain.setValueAtTime(intensity, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.1);
        
        const filter = this.audioContext.createBiquadFilter();
        filter.type = 'highpass';
        filter.frequency.value = 1000;
        
        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.destination);
        
        noise.start(time);
        noise.stop(time + 0.1);
      }
    };
  }
  
  createHatSynth() {
    return {
      trigger: (time, intensity) => {
        const osc1 = this.audioContext.createOscillator();
        const osc2 = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        
        osc1.type = 'square';
        osc2.type = 'square';
        osc1.frequency.value = 300;
        osc2.frequency.value = 315;
        
        gain.gain.setValueAtTime(intensity * 0.5, time);
        gain.gain.exponentialRampToValueAtTime(0.001, time + 0.05);
        
        const filter = this.audioContext.createBiquadFilter();
        filter.type = 'highpass';
        filter.frequency.value = 5000;
        
        osc1.connect(filter);
        osc2.connect(filter);
        filter.connect(gain);
        gain.connect(this.destination);
        
        osc1.start(time);
        osc2.start(time);
        osc1.stop(time + 0.05);
        osc2.stop(time + 0.05);
      }
    };
  }
}

// ═══════════════════════════════════════
// EXPORT
// ═══════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { MemorySonificationEngine };
}
