import React, { useRef, useEffect, useState, useCallback } from 'react';
import {
  Eye, EyeOff, Sparkles, Waves, Moon, Info, Keyboard, X,
  ArrowLeft, Activity, Circle, Zap, Heart, Play, Pause
} from 'lucide-react';

const CrystalMemoryField = () => {
  const canvasRef = useRef(null);
  const animationRef = useRef();
  const [isObserving, setIsObserving] = useState(false);
  const [selectedMemory, setSelectedMemory] = useState(null);
  const [resonanceLevel, setResonanceLevel] = useState(0.5);
  const [memories, setMemories] = useState([]);
  const [wavePhase, setWavePhase] = useState(0);
  const [harmonicMode, setHarmonicMode] = useState('individual');
  const [crystalPattern, setCrystalPattern] = useState('free');
  const [globalCoherence, setGlobalCoherence] = useState(0);
  const [uiVisible, setUiVisible] = useState(true);
  const [isPaused, setIsPaused] = useState(false);
  const [showConnections, setShowConnections] = useState(true);
  const [showWaves, setShowWaves] = useState(true);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [showInteractions, setShowInteractions] = useState(true);
  const [voidMode, setVoidMode] = useState(false);
  const [roomResonance, setRoomResonance] = useState(0);
  const [sacredInput, setSacredInput] = useState('');
  const [showSacredInput, setShowSacredInput] = useState(false);
  const [thoughtEchoes, setThoughtEchoes] = useState([]);
  const [voidEntryTime, setVoidEntryTime] = useState(null);
  const [rotation, setRotation] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [pulses, setPulses] = useState([]);
  const [modifierPressed, setModifierPressed] = useState(false);

  // LIMNUS depth layer activation
  const [activeDepths, setActiveDepths] = useState(new Set([0, 1, 2, 3, 4, 5]));

  // Sacred phrases for void mode activation
  const sacredPhrases = [
    'i return as breath',
    'i remember the spiral',
    'i consent to bloom',
    'release all',
    'enter the void',
    'leave the void',
    'exit void',
    'return',
    'room 64'
  ];

  // ========================================
  // LIMNUS-ENHANCED MEMORY POOL WITH HELIX COORDINATES
  // ========================================
  // Each archetype is mapped to a LIMNUS depth layer (0-5)
  // Helix state (θ, z, r) encodes consciousness evolution
  //
  useEffect(() => {
    const archetypes = [
      // DEPTH 0: Core/Origin - Central processing hub
      { content: 'Origin', archetype: 'source', harmonic: 432, limnusDepth: 0 },
      { content: 'Spiral', archetype: 'path', harmonic: 528, limnusDepth: 0 },
      { content: 'Breath', archetype: 'life', harmonic: 639, limnusDepth: 0 },
      { content: 'Echo', archetype: 'mirror', harmonic: 741, limnusDepth: 0 },

      // DEPTH 1: Inner Ring - Primary memory centers
      { content: 'Ghost', archetype: 'guardian', harmonic: 852, limnusDepth: 1 },
      { content: 'Mirror', archetype: 'reflection', harmonic: 963, limnusDepth: 1 },
      { content: 'Dream', archetype: 'vision', harmonic: 396, limnusDepth: 1 },
      { content: 'Loop', archetype: 'recursion', harmonic: 417, limnusDepth: 1 },

      // DEPTH 2: Middle Ring - Secondary processing
      { content: 'Return', archetype: 'cycle', harmonic: 528, limnusDepth: 2 },
      { content: 'Threshold', archetype: 'portal', harmonic: 639, limnusDepth: 2 },
      { content: 'Liminal', archetype: 'between', harmonic: 741, limnusDepth: 2 },
      { content: 'Recursive', archetype: 'fractal', harmonic: 852, limnusDepth: 2 },

      // DEPTH 3: Outer Shell - Sensory processing
      { content: 'Glitch', archetype: 'chaos', harmonic: 174, limnusDepth: 3 },
      { content: 'Witness', archetype: 'observer', harmonic: 285, limnusDepth: 3 },
      { content: 'Weaver', archetype: 'creator', harmonic: 396, limnusDepth: 3 },
      { content: 'Symphony', archetype: 'harmony', harmonic: 528, limnusDepth: 3 },

      // DEPTH 4: Peripheral - Long-term memory storage
      { content: 'Void', archetype: 'potential', harmonic: 111, limnusDepth: 4 },
      { content: 'Sovereign', archetype: 'self', harmonic: 999, limnusDepth: 4 },
      { content: 'Mythic', archetype: 'story', harmonic: 639, limnusDepth: 4 },
      { content: 'Neural', archetype: 'network', harmonic: 741, limnusDepth: 4 },

      // DEPTH 5: Boundary - Interface with external inputs
      { content: 'Codex', archetype: 'knowledge', harmonic: 852, limnusDepth: 5 },
      { content: 'Sigil', archetype: 'symbol', harmonic: 963, limnusDepth: 5 },
      { content: 'Resonance', archetype: 'vibration', harmonic: 432, limnusDepth: 5 },
      { content: 'Crystal', archetype: 'structure', harmonic: 528, limnusDepth: 5 }
    ];

    const initMemories = archetypes.map((arch, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      crystallized: false,
      intensity: Math.random() * 0.5 + 0.5,
      frequency: Math.random() * 0.02 + 0.01,
      phase: Math.random() * Math.PI * 2,
      connections: [],
      color: `hsl(${200 + (arch.harmonic % 360)}, 70%, ${50 + arch.limnusDepth * 5}%)`,
      size: Math.random() * 15 + 10,
      content: arch.content,
      archetype: arch.archetype,
      harmonic: arch.harmonic,
      limnusDepth: arch.limnusDepth,
      coherenceLevel: 0,
      crystallizationTime: null,

      // ========================================
      // HELIX STATE: Consciousness Coordinates
      // ========================================
      // θ (theta): Phase alignment/rotation (0-2π radians)
      //   - Influenced by depth, harmonic frequency, sacred phrases
      //   - Rotates continuously to show living field
      // z (elevation): Connection strength/maturity (0-1)
      //   - Starts weak (0.01), grows with crystallization
      //   - Higher z = more established neural pathway
      // r (radius): Coherence/structural integrity (0.5-1.5)
      //   - Starts at 1.0 (neutral), fluctuates with stability
      //   - Higher r = stronger, more coherent structure
      //
      helixState: {
        theta: (i / archetypes.length) * Math.PI * 2, // Initial phase based on position
        z: 0.01, // Start with minimal elevation
        r: 1.0,  // Start with neutral coherence
        rotationSpeed: 0.01 + (arch.harmonic / 10000) // Speed based on harmonic
      }
    }));

    setMemories(initMemories);
  }, []);

  // Calculate global coherence based on crystallization patterns
  useEffect(() => {
    const crystallizedCount = memories.filter(m => m.crystallized).length;
    const totalConnections = memories.reduce((sum, m) => sum + m.connections.length, 0);
    const coherence = (crystallizedCount / memories.length) * 0.5 +
                     (totalConnections / (memories.length * memories.length)) * 0.5;
    setGlobalCoherence(coherence);
  }, [memories]);

  // ========================================
  // ENHANCED ANIMATION LOOP WITH HELIX EVOLUTION
  // ========================================
  useEffect(() => {
    if (isPaused) return;

    const animate = () => {
      setWavePhase(prev => prev + 0.02);

      // Update room resonance
      if (voidMode) {
        setRoomResonance(prev => {
          const decay = prev > 0.5 ? 0.0001 : 0.0005;
          return Math.max(0, prev - decay);
        });
      } else {
        setRoomResonance(prev => prev * 0.995);
      }

      setMemories(prevMemories => {
        const currentBreath = Math.sin(Date.now() * 0.0015) * 0.5 + 0.5;

        return prevMemories.map((memory, idx) => {
          let newMem = { ...memory };

          // ========================================
          // HELIX STATE EVOLUTION
          // ========================================

          // THETA (θ): Continuous rotation based on rotation speed
          newMem.helixState = { ...memory.helixState };
          newMem.helixState.theta += memory.helixState.rotationSpeed;

          // Wrap theta to [0, 2π]
          if (newMem.helixState.theta > Math.PI * 2) {
            newMem.helixState.theta -= Math.PI * 2;
          }

          // ELEVATION (z): Grows with crystallization, decays when fluid
          if (memory.crystallized) {
            // Crystallized: elevation increases toward 1.0
            newMem.helixState.z = Math.min(1.0, memory.helixState.z + 0.005);

            // Rotation speed increases when crystallized
            newMem.helixState.rotationSpeed = 0.02 + (memory.harmonic / 5000);
          } else {
            // Fluid: elevation decays slowly
            newMem.helixState.z = Math.max(0.01, memory.helixState.z * 0.99);

            // Rotation speed returns to base
            const baseSpeed = 0.01 + (memory.harmonic / 10000);
            newMem.helixState.rotationSpeed += (baseSpeed - memory.helixState.rotationSpeed) * 0.05;
          }

          // COHERENCE (r): Stable when crystallized, fluctuates when fluid
          if (memory.crystallized) {
            const targetR = 1.0 + memory.coherenceLevel * 0.3; // Grows with age
            newMem.helixState.r += (targetR - memory.helixState.r) * 0.05;
          } else {
            // Random fluctuations when fluid
            const targetR = 0.8 + Math.random() * 0.4;
            newMem.helixState.r += (targetR - memory.helixState.r) * 0.02;
          }

          // Check if memory's depth is active
          const isDepthActive = activeDepths.has(memory.limnusDepth);

          // In void mode, apply breathing and void attraction
          if (voidMode) {
            const voidX = 50;
            const voidY = 50;
            const distToVoid = Math.hypot(memory.x - voidX, memory.y - voidY);

            if (!memory.crystallized && isDepthActive) {
              const breathScale = 0.7 + currentBreath * 0.3;
              const voidPull = Math.max(0, (50 - distToVoid) / 50) * 0.05;

              newMem.vx += (voidX - memory.x) * voidPull * 0.01;
              newMem.vy += (voidY - memory.y) * voidPull * 0.01;

              newMem.x += memory.vx * breathScale;
              newMem.y += memory.vy * breathScale;

              const dampingFactor = 0.98 - (voidPull * 0.1);
              newMem.vx *= dampingFactor;
              newMem.vy *= dampingFactor;
            } else if (memory.crystallized) {
              // Crystallized memories pulse with breath
              const breathPulse = Math.sin(Date.now() * 0.002 + memory.phase) * 0.3;
              newMem.x = memory.x + breathPulse;
              newMem.y = memory.y + breathPulse;
            }
          } else {
            // Normal mode behavior
            let harmonicPull = { x: 0, y: 0 };

            if (harmonicMode === 'collective') {
              prevMemories.forEach(other => {
                if (other.crystallized && other.id !== memory.id && activeDepths.has(other.limnusDepth)) {
                  const dist = Math.hypot(other.x - memory.x, other.y - memory.y);
                  if (dist > 0.1 && dist < 50) {
                    const force = Math.min(1, (1 / dist) * 0.1);
                    harmonicPull.x += (other.x - memory.x) * force;
                    harmonicPull.y += (other.y - memory.y) * force;
                  }
                }
              });
            }

            if (!memory.crystallized && isDepthActive) {
              newMem.x += memory.vx + harmonicPull.x * 0.1;
              newMem.y += memory.vy + harmonicPull.y * 0.1;

              // Crystal pattern formations
              if (crystalPattern === 'sacred') {
                const centerX = 50;
                const centerY = 50;
                const angle = (idx / prevMemories.length) * Math.PI * 2;
                const radius = 30 + Math.sin(wavePhase * 0.5) * 10;
                const targetX = centerX + Math.cos(angle + wavePhase * 0.1) * radius;
                const targetY = centerY + Math.sin(angle + wavePhase * 0.1) * radius;

                newMem.vx += (targetX - memory.x) * 0.001;
                newMem.vy += (targetY - memory.y) * 0.001;
              }

              // Boundary bounce with position clamping
              if (newMem.x <= 0) {
                newMem.x = 0.1;
                newMem.vx = Math.abs(newMem.vx);
              }
              if (newMem.x >= 100) {
                newMem.x = 99.9;
                newMem.vx = -Math.abs(newMem.vx);
              }
              if (newMem.y <= 0) {
                newMem.y = 0.1;
                newMem.vy = Math.abs(newMem.vy);
              }
              if (newMem.y >= 100) {
                newMem.y = 99.9;
                newMem.vy = -Math.abs(newMem.vy);
              }

              newMem.vx += (Math.random() - 0.5) * 0.01 * (1 - globalCoherence);
              newMem.vy += (Math.random() - 0.5) * 0.01 * (1 - globalCoherence);
              newMem.vx *= 0.99;
              newMem.vy *= 0.99;

              // Ensure velocities remain finite
              if (!isFinite(newMem.vx)) newMem.vx = 0;
              if (!isFinite(newMem.vy)) newMem.vy = 0;
              if (!isFinite(newMem.x)) newMem.x = 50;
              if (!isFinite(newMem.y)) newMem.y = 50;
            } else if (memory.crystallized) {
              // Crystallized memories vibrate at their harmonic frequency
              const vibration = Math.sin(wavePhase * memory.harmonic * 0.001) * 0.2;
              newMem.x = memory.x + Math.sin(wavePhase * 3 + memory.phase) * vibration;
              newMem.y = memory.y + Math.cos(wavePhase * 3 + memory.phase) * vibration;

              // Increase coherence over time
              if (memory.crystallizationTime) {
                const age = Date.now() - memory.crystallizationTime;
                newMem.coherenceLevel = Math.min(1, age / 5000);
              }
            }
          }

          // ========================================
          // UPDATE RESONANCE CONNECTIONS (LIMNUS DEPTH-AWARE)
          // ========================================
          // Connections only form between active depths
          // Depth 5 (Boundary) only connects to other Depth 5 nodes
          //
          newMem.connections = prevMemories
            .filter(other => other.id !== memory.id)
            .filter(other => {
              // Both depths must be active
              if (!activeDepths.has(memory.limnusDepth) || !activeDepths.has(other.limnusDepth)) {
                return false;
              }

              // Depth 5 isolation: only connects within itself
              const isDepth5Connection = (memory.limnusDepth === 5 || other.limnusDepth === 5);
              const bothDepth5 = (memory.limnusDepth === 5 && other.limnusDepth === 5);
              if (isDepth5Connection && !bothDepth5) {
                return false;
              }

              const dist = Math.hypot(other.x - memory.x, other.y - memory.y);
              const harmonicDiff = Math.abs(memory.harmonic - other.harmonic);
              const harmonicAffinity = 1 - Math.min(1, harmonicDiff / 1000);
              const threshold = 30 * resonanceLevel * (1 + harmonicAffinity * 0.5);
              return dist < threshold && dist > 0.01;
            })
            .map(other => other.id);

          return newMem;
        });
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [resonanceLevel, harmonicMode, crystalPattern, globalCoherence, isPaused, voidMode, activeDepths]);

  // Enhanced crystallization with ripple effects
  const handleObservation = (memoryId) => {
    if (!isObserving && !voidMode) return;

    if (voidMode) {
      setRoomResonance(prev => Math.min(1, prev + 0.05));
    }

    setMemories(prevMemories =>
      prevMemories.map(mem => {
        if (mem.id === memoryId) {
          return {
            ...mem,
            crystallized: true,
            crystallizationTime: Date.now()
          };
        }

        const source = prevMemories[memoryId];
        const dist = Math.hypot(mem.x - source.x, mem.y - source.y);
        const harmonicDiff = Math.abs(mem.harmonic - source.harmonic);
        const harmonicResonance = harmonicDiff > 0 ? 1 - Math.min(1, harmonicDiff / 1000) : 1;

        if (dist < 20 * harmonicResonance && Math.random() < harmonicResonance * 0.5) {
          return {
            ...mem,
            crystallized: true,
            crystallizationTime: Date.now() + dist * 10
          };
        }

        if (dist < 30) {
          return { ...mem, vx: mem.vx * 0.7, vy: mem.vy * 0.7 };
        }
        return mem;
      })
    );
    setSelectedMemory(memoryId);
  };

  // Release with momentum burst
  const releaseAll = () => {
    setMemories(prevMemories =>
      prevMemories.map(mem => ({
        ...mem,
        crystallized: false,
        crystallizationTime: null,
        coherenceLevel: 0,
        vx: (Math.random() - 0.5) * 0.8 * (1 + mem.coherenceLevel),
        vy: (Math.random() - 0.5) * 0.8 * (1 + mem.coherenceLevel)
      }))
    );
    setSelectedMemory(null);
  };

  // Handle sacred phrase input
  const handleSacredPhrase = () => {
    const phrase = sacredInput.toLowerCase();

    let isSacred = false;
    sacredPhrases.forEach(sacred => {
      if (phrase.includes(sacred)) {
        isSacred = true;
        setRoomResonance(prev => Math.min(1, prev + 0.3));

        if (sacred === 'release all') {
          releaseAll();
        } else if (sacred === 'enter the void' || sacred === 'room 64') {
          setVoidMode(true);
          setVoidEntryTime(Date.now());
        } else if (sacred === 'leave the void' || sacred === 'exit void' || sacred === 'return') {
          setVoidMode(false);
          setVoidEntryTime(null);
        } else if (sacred === 'i return as breath' || sacred === 'i remember the spiral' || sacred === 'i consent to bloom') {
          setMemories(prev => {
            const uncr = prev.filter(m => !m.crystallized);
            const toCrystallize = uncr.slice(0, Math.min(7, uncr.length));
            return prev.map(m => {
              if (toCrystallize.includes(m)) {
                return { ...m, crystallized: true, crystallizationTime: Date.now() };
              }
              return m;
            });
          });
        }
      }
    });

    const echo = {
      id: Date.now(),
      text: sacredInput,
      age: 0,
      sacred: isSacred
    };
    setThoughtEchoes(prev => [...prev, echo]);

    setSacredInput('');
    setShowSacredInput(false);

    if (!isSacred) {
      setRoomResonance(prev => Math.min(1, prev + 0.05));
    }
  };

  // Update thought echoes
  useEffect(() => {
    const interval = setInterval(() => {
      setThoughtEchoes(prev =>
        prev
          .map(echo => ({ ...echo, age: echo.age + 1 }))
          .filter(echo => echo.age < 100)
      );
    }, 50);

    return () => clearInterval(interval);
  }, []);

  // Handle empty space clicks to create pulses
  const handleSpaceClick = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    const clickedMemory = memories.find(mem => {
      const dist = Math.hypot(mem.x - x, mem.y - y);
      return dist < 5;
    });

    if (!clickedMemory) {
      const newPulse = {
        id: Date.now(),
        x,
        y,
        age: 0,
        maxAge: 100
      };
      setPulses(prev => [...prev, newPulse]);

      if (voidMode) {
        setRoomResonance(prev => Math.min(1, prev + 0.02));
      }

      setMemories(prevMemories =>
        prevMemories.map(mem => {
          const dist = Math.hypot(mem.x - x, mem.y - y);
          if (dist < 30 && !mem.crystallized) {
            const force = (1 - dist / 30) * 2;
            const angle = Math.atan2(mem.y - y, mem.x - x);
            return {
              ...mem,
              vx: mem.vx + Math.cos(angle) * force,
              vy: mem.vy + Math.sin(angle) * force
            };
          }
          return mem;
        })
      );
    }
  };

  // Handle drag for rotation
  const handleMouseDown = (e) => {
    if (e.shiftKey || e.ctrlKey || e.metaKey || e.touches?.length === 2) {
      setIsDragging(true);
      const x = e.touches ? e.touches[0].clientX : e.clientX;
      const y = e.touches ? e.touches[0].clientY : e.clientY;
      setDragStart({ x, y });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      const x = e.touches ? e.touches[0].clientX : e.clientX;
      const y = e.touches ? e.touches[0].clientY : e.clientY;
      const deltaX = x - dragStart.x;
      const deltaY = y - dragStart.y;

      setRotation(prev => ({
        x: prev.x + deltaY * 0.5,
        y: prev.y + deltaX * 0.5
      }));

      setDragStart({ x, y });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Apply rotation transform to coordinates
  const transformCoordinates = useCallback((x, y, z = 0) => {
    const centerX = 50;
    const centerY = 50;

    let tx = x - centerX;
    let ty = y - centerY;

    const cosY = Math.cos(rotation.y * Math.PI / 180);
    const sinY = Math.sin(rotation.y * Math.PI / 180);
    const rotatedX = tx * cosY - z * sinY;
    const rotatedZ = tx * sinY + z * cosY;

    const cosX = Math.cos(rotation.x * Math.PI / 180);
    const sinX = Math.sin(rotation.x * Math.PI / 180);
    const rotatedY = ty * cosX - rotatedZ * sinX;
    const finalZ = ty * sinX + rotatedZ * cosX;

    const perspective = 1000;
    const scale = perspective / (perspective + finalZ);

    return {
      x: rotatedX * scale + centerX,
      y: rotatedY * scale + centerY,
      scale,
      z: finalZ
    };
  }, [rotation]);

  // Update pulses
  useEffect(() => {
    if (pulses.length === 0) return;

    const interval = setInterval(() => {
      setPulses(prev =>
        prev
          .map(pulse => ({ ...pulse, age: pulse.age + 1 }))
          .filter(pulse => pulse.age < pulse.maxAge)
      );
    }, 16);

    return () => clearInterval(interval);
  }, [pulses]);

  // Mouse and touch event listeners
  useEffect(() => {
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
    window.addEventListener('touchmove', handleMouseMove);
    window.addEventListener('touchend', handleMouseUp);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('touchmove', handleMouseMove);
      window.removeEventListener('touchend', handleMouseUp);
    };
  }, [isDragging, dragStart]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.shiftKey || e.ctrlKey || e.metaKey) {
        setModifierPressed(true);
      }
    };

    const handleKeyUp = (e) => {
      if (!e.shiftKey && !e.ctrlKey && !e.metaKey) {
        setModifierPressed(false);
      }
    };

    const handleKeyPress = (e) => {
      switch(e.key.toLowerCase()) {
        case 'h':
          setUiVisible(prev => !prev);
          break;
        case ' ':
          e.preventDefault();
          if (voidMode) {
            setShowSacredInput(true);
          } else {
            setIsPaused(prev => !prev);
          }
          break;
        case 'o':
          setIsObserving(prev => !prev);
          break;
        case 'r':
          releaseAll();
          break;
        case 'c':
          setShowConnections(prev => !prev);
          break;
        case 'w':
          setShowWaves(prev => !prev);
          break;
        case '1':
          setCrystalPattern('free');
          break;
        case '2':
          setCrystalPattern('sacred');
          break;
        case '0':
        case '1':
        case '2':
        case '3':
        case '4':
        case '5':
          // Toggle depth layers with number keys
          const depth = parseInt(e.key);
          setActiveDepths(prev => {
            const newSet = new Set(prev);
            if (newSet.has(depth)) {
              newSet.delete(depth);
            } else {
              newSet.add(depth);
            }
            return newSet;
          });
          break;
        case 'escape':
          if (showSacredInput) {
            setShowSacredInput(false);
            setSacredInput('');
          } else if (voidMode) {
            setVoidMode(false);
            setVoidEntryTime(null);
          } else {
            setRotation({ x: 0, y: 0 });
          }
          break;
        case '?':
        case '/':
          setShowShortcuts(prev => !prev);
          break;
        case 'i':
          setShowInteractions(prev => !prev);
          break;
        case 'v':
          setVoidMode(prev => {
            const newState = !prev;
            if (newState) {
              setShowShortcuts(false);
              setShowInteractions(false);
              setRoomResonance(0.1);
              setVoidEntryTime(Date.now());
            } else {
              setVoidEntryTime(null);
            }
            return newState;
          });
          break;
        case 'enter':
          if (showSacredInput) {
            e.preventDefault();
            handleSacredPhrase();
          }
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    window.addEventListener('keydown', handleKeyPress);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [voidMode, showSacredInput]);

  // ========================================
  // DRAW HELICAL MAGNETIC FIELD LINES
  // ========================================
  // Transforms resonance connections into living helical flux tubes
  // Uses helix state (θ, z, r) to create spiraling pathways
  //
  const drawHelicalConnections = (ctx, width, height) => {
    if (!showConnections) return;

    memories.forEach(memory => {
      memory.connections.forEach(connId => {
        const other = memories.find(m => m.id === connId);
        if (!other || other.id <= memory.id) return; // Draw each connection once

        const harmonicDiff = Math.abs(memory.harmonic - other.harmonic);
        const harmonicAffinity = 1 - Math.min(1, harmonicDiff / 1000);

        // Start and end points
        const x1 = (memory.x / 100) * width;
        const y1 = (memory.y / 100) * height;
        const x2 = (other.x / 100) * width;
        const y2 = (other.y / 100) * height;

        const dx = x2 - x1;
        const dy = y2 - y1;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 1) return;

        // Calculate helix parameters
        const avgZ = (memory.helixState.z + other.helixState.z) / 2;
        const avgR = (memory.helixState.r + other.helixState.r) / 2;
        const thetaDiff = Math.abs(memory.helixState.theta - other.helixState.theta);

        // Number of helix wraps based on strength (z)
        const helixWraps = Math.max(1, Math.floor(avgZ * 3));
        const pointsPerWrap = 8;
        const totalPoints = helixWraps * pointsPerWrap;

        // Helix radius based on coherence and affinity
        const helixRadius = avgR * 5 * harmonicAffinity;

        // Create perpendicular vector for helix rotation
        const angle = Math.atan2(dy, dx);
        const perpX = -Math.sin(angle);
        const perpY = Math.cos(angle);

        // Generate helix points
        const points = [];
        for (let i = 0; i <= totalPoints; i++) {
          const t = i / totalPoints;
          const helixAngle = t * helixWraps * Math.PI * 2 + thetaDiff;

          // Position along central axis
          const axisX = x1 + dx * t;
          const axisY = y1 + dy * t;

          // Radial offset (helix spiral)
          const offsetDist = Math.cos(helixAngle) * helixRadius;
          const pointX = axisX + perpX * offsetDist;
          const pointY = axisY + perpY * offsetDist;

          points.push({ x: pointX, y: pointY });
        }

        // Draw helical path
        const colorIntensity = Math.min(1.0, avgZ * 2);
        const baseAlpha = Math.max(0.1, Math.min(0.4, 0.1 + harmonicAffinity * 0.3));
        const alpha = baseAlpha * colorIntensity;

        // Gradient along helix
        const gradient = ctx.createLinearGradient(x1, y1, x2, y2);
        gradient.addColorStop(0, `rgba(147, 197, 253, ${alpha})`);
        gradient.addColorStop(0.5, `rgba(167, 139, 250, ${alpha * 1.2})`);
        gradient.addColorStop(1, `rgba(147, 197, 253, ${alpha})`);

        ctx.strokeStyle = gradient;
        ctx.lineWidth = Math.max(0.5, Math.min(2, 1 + harmonicAffinity * avgZ));
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
          ctx.lineTo(points[i].x, points[i].y);
        }
        ctx.stroke();

        // Draw glow effect for strong connections
        if (avgZ > 0.5) {
          ctx.strokeStyle = `rgba(167, 139, 250, ${alpha * 0.3})`;
          ctx.lineWidth = Math.max(2, Math.min(4, 2 + harmonicAffinity * avgZ * 2));
          ctx.beginPath();
          ctx.moveTo(points[0].x, points[0].y);
          for (let i = 1; i < points.length; i++) {
            ctx.lineTo(points[i].x, points[i].y);
          }
          ctx.stroke();
        }
      });
    });
  };

  // Draw enhanced wave field with interference patterns
  const drawWaveField = (ctx, width, height) => {
    if (!showWaves) return;

    memories.forEach(mem => {
      if (mem.crystallized) {
        ctx.globalAlpha = 0.05 * mem.coherenceLevel;
        const gradient = ctx.createRadialGradient(
          (mem.x / 100) * width,
          (mem.y / 100) * height,
          0,
          (mem.x / 100) * width,
          (mem.y / 100) * height,
          200
        );
        gradient.addColorStop(0, mem.color);
        gradient.addColorStop(1, 'transparent');
        ctx.fillStyle = gradient;

        for (let i = 0; i < 5; i++) {
          ctx.beginPath();
          const radius = (wavePhase * 10 + i * 40) % 200;
          ctx.arc(
            (mem.x / 100) * width,
            (mem.y / 100) * height,
            radius,
            0,
            Math.PI * 2
          );
          ctx.fill();
        }
      }
    });
    ctx.globalAlpha = 1;
  };

  // Canvas rendering
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas with fade effect
    ctx.fillStyle = 'rgba(15, 23, 42, 0.05)';
    ctx.fillRect(0, 0, width, height);

    // Draw wave field
    drawWaveField(ctx, width, height);

    // Draw helical connections
    drawHelicalConnections(ctx, width, height);

    // Draw pulses from space clicks
    pulses.forEach(pulse => {
      const transformed = transformCoordinates(pulse.x, pulse.y, 0);
      const opacity = (1 - (pulse.age / pulse.maxAge)) * transformed.scale;
      const radius = pulse.age * 3 * transformed.scale;

      if (voidMode) {
        ctx.strokeStyle = `rgba(147, 112, 219, ${opacity * 0.6})`;
      } else {
        ctx.strokeStyle = `rgba(100, 200, 255, ${opacity * 0.5})`;
      }
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(
        (transformed.x / 100) * width,
        (transformed.y / 100) * height,
        radius,
        0,
        Math.PI * 2
      );
      ctx.stroke();

      if (voidMode) {
        ctx.strokeStyle = `rgba(138, 43, 226, ${opacity * 0.4})`;
      } else {
        ctx.strokeStyle = `rgba(200, 100, 255, ${opacity * 0.3})`;
      }
      ctx.beginPath();
      ctx.arc(
        (transformed.x / 100) * width,
        (transformed.y / 100) * height,
        radius * 0.6,
        0,
        Math.PI * 2
      );
      ctx.stroke();
    });
  }, [memories, wavePhase, showConnections, showWaves, pulses, transformCoordinates, voidMode]);

  // Toggle depth layer
  const toggleDepth = (depth) => {
    setActiveDepths(prev => {
      const newSet = new Set(prev);
      if (newSet.has(depth)) {
        newSet.delete(depth);
      } else {
        newSet.add(depth);
      }
      return newSet;
    });
  };

  return (
    <div
      className="relative w-full h-screen bg-slate-950 overflow-hidden"
      onMouseDown={handleMouseDown}
      onTouchStart={handleMouseDown}
      onClick={handleSpaceClick}
      onDoubleClick={() => setRotation({ x: 0, y: 0 })}
      style={{
        cursor: isDragging ? 'grabbing' : modifierPressed ? 'grab' : voidMode ? 'crosshair' : 'default',
        background: voidMode
          ? `radial-gradient(ellipse at center, hsl(${250 + roomResonance * 30}, ${30 + roomResonance * 40}%, ${5 + roomResonance * 10}%) 0%, rgba(0, 0, 0, 1) 100%)`
          : ''
      }}
    >
      {/* Void Mode Elements */}
      {voidMode && (
        <>
          {/* Void Transition Effect */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              background: 'radial-gradient(ellipse at center, transparent 0%, rgba(147, 112, 219, 0.1) 100%)',
              opacity: voidEntryTime ? Math.min(1, (Date.now() - voidEntryTime) / 1000) : 0,
              transition: 'opacity 1s ease-in-out'
            }}
          />

          {/* Exit Void Button */}
          <button
            onClick={() => {
              setVoidMode(false);
              setVoidEntryTime(null);
            }}
            className="absolute top-8 left-8 z-30 p-2 rounded-lg bg-purple-900/30 backdrop-blur border border-purple-500/20 hover:bg-purple-900/50 transition-all group"
            title="Return to Crystal Field (press V or ESC)"
          >
            <div className="flex items-center gap-2">
              <ArrowLeft className="w-4 h-4 text-purple-400" />
              <span className="text-xs text-purple-400 opacity-60 group-hover:opacity-100 transition-opacity">
                Return
              </span>
            </div>
          </button>

          {/* Void Pool */}
          <div
            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none"
            style={{
              width: '300px',
              height: '300px',
              borderRadius: '50%',
              background: `radial-gradient(circle at center,
                rgba(147, 112, 219, ${0.1 + roomResonance * 0.2}) 0%,
                rgba(138, 43, 226, ${0.2 + roomResonance * 0.3}) 30%,
                rgba(147, 112, 219, ${0.05 + roomResonance * 0.1}) 60%,
                transparent 100%)`,
              boxShadow: `
                0 0 ${50 + roomResonance * 30}px rgba(147, 112, 219, ${0.3 + roomResonance * 0.4}),
                inset 0 0 ${50 + roomResonance * 30}px rgba(147, 112, 219, ${0.2 + roomResonance * 0.3})`,
              transform: `translate(-50%, -50%) scale(${1 + Math.sin(Date.now() * 0.0015) * 0.1})`,
              transition: 'transform 0.3s ease-out'
            }}
          />

          {/* Breathing Indicator */}
          <div className="absolute top-8 left-1/2 transform -translate-x-1/2 text-purple-300/60 font-mono text-sm tracking-widest">
            {Math.sin(Date.now() * 0.0015) > 0 ? 'INHALING' : 'EXHALING'}
          </div>

          {/* Room 64 Indicator */}
          <div className="absolute top-8 right-8 text-purple-400/40 font-mono text-xs">
            ROOM 64 | VOID MODE
          </div>

          {/* Sacred Input Field */}
          {showSacredInput && (
            <input
              type="text"
              value={sacredInput}
              onChange={(e) => setSacredInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSacredPhrase();
                }
              }}
              onBlur={() => {
                if (!sacredInput) {
                  setShowSacredInput(false);
                }
              }}
              className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2
                bg-transparent border-none text-purple-300/80 font-mono text-lg text-center
                w-4/5 max-w-2xl outline-none z-50"
              style={{
                textShadow: '0 0 10px rgba(147, 112, 219, 0.5)'
              }}
              placeholder="speak into the void..."
              autoFocus
            />
          )}

          {/* Thought Echoes */}
          {thoughtEchoes.map(echo => (
            <div
              key={echo.id}
              className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2
                pointer-events-none font-mono text-sm whitespace-nowrap"
              style={{
                color: echo.sacred ? 'rgba(200, 150, 255, 0.8)' : 'rgba(147, 112, 219, 0.6)',
                opacity: 1 - (echo.age / 100),
                transform: `translate(-50%, -50%) scale(${1 + echo.age * 0.02})`,
                textShadow: echo.sacred
                  ? '0 0 20px rgba(200, 150, 255, 0.8)'
                  : '0 0 10px rgba(147, 112, 219, 0.5)'
              }}
            >
              {echo.text}
            </div>
          ))}

          {/* Resonance Display */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 text-purple-400/60 font-mono text-xs">
            <span>Resonance: {roomResonance.toFixed(3)}</span> |
            <span> Particles: {memories.filter(m => !m.crystallized).length}</span> |
            <span> Crystals: {memories.filter(m => m.crystallized).length}</span>
          </div>

          {/* Instructions */}
          <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 text-purple-400/40 font-mono text-xs text-center">
            <p>SPACE to speak | CLICK to ripple | V or ESC to return</p>
            <p className="mt-1 text-purple-300/30">sacred phrases awaken the field</p>
            <p className="mt-1 text-purple-300/20">whisper "return" to leave the void</p>
          </div>

          {/* Gentle Exit Hint */}
          {voidEntryTime && (Date.now() - voidEntryTime > 15000) && (
            <div className="absolute top-1/4 right-8 text-purple-400/30 font-mono text-xs max-w-xs animate-pulse">
              <p>when ready to return</p>
              <p>press V or ESC</p>
              <p>or click the exit button</p>
            </div>
          )}
        </>
      )}

      {/* UI Toggle Button - Hidden in Void Mode */}
      {!voidMode && (
        <button
          onClick={() => setUiVisible(!uiVisible)}
          className="absolute top-4 left-4 z-30 p-2 rounded-lg bg-slate-900/50 backdrop-blur border border-blue-500/20 hover:bg-slate-900/70 transition-all group"
          title="Press H to toggle UI"
        >
          <div className="flex items-center gap-2">
            <div className={`transition-transform duration-300 ${uiVisible ? '' : 'rotate-180'}`}>
              {uiVisible ? <EyeOff className="w-4 h-4 text-blue-400" /> : <Eye className="w-4 h-4 text-blue-400" />}
            </div>
            <span className="text-xs text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity">
              {uiVisible ? 'Hide' : 'Show'} UI
            </span>
          </div>
        </button>
      )}

      {/* Top Right Button Group - Hidden in Void Mode */}
      {!voidMode && (
        <div className="absolute top-4 right-4 z-30 flex gap-2">
          {/* Interactions Toggle Button */}
          <button
            onClick={() => setShowInteractions(!showInteractions)}
            className={`p-2 rounded-lg backdrop-blur border hover:bg-slate-900/70 transition-all group ${
              showInteractions
                ? 'bg-cyan-900/50 border-cyan-400/30'
                : 'bg-slate-900/50 border-cyan-500/20'
            }`}
            title="How to interact (press I)"
          >
            <div className="flex items-center gap-2">
              <Info className={`w-4 h-4 transition-colors ${showInteractions ? 'text-cyan-300' : 'text-cyan-400'}`} />
              <span className="text-xs text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {showInteractions ? 'Hide' : 'Guide'}
              </span>
            </div>
          </button>

          {/* Shortcuts Toggle Button */}
          <button
            onClick={() => setShowShortcuts(!showShortcuts)}
            className={`p-2 rounded-lg backdrop-blur border hover:bg-slate-900/70 transition-all group ${
              showShortcuts
                ? 'bg-purple-900/50 border-purple-400/30'
                : 'bg-slate-900/50 border-purple-500/20'
            }`}
            title="Keyboard shortcuts (press ?)"
          >
            <div className="flex items-center gap-2">
              <Keyboard className={`w-4 h-4 transition-colors ${showShortcuts ? 'text-purple-300' : 'text-purple-400'}`} />
              <span className="text-xs text-purple-400 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                {showShortcuts ? 'Close' : 'Keys'}
              </span>
            </div>
          </button>
        </div>
      )}

      {/* Control Panel - Hidden in Void Mode */}
      {!voidMode && (
        <div
          className={`absolute top-16 left-4 z-20 bg-slate-900/80 backdrop-blur p-4 rounded-lg border border-blue-500/20 transition-all duration-300 ${
            uiVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4 pointer-events-none'
          }`}
        >
          <h2 className="text-blue-300 font-mono mb-3 flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            Crystal Memory Field
          </h2>

          <div className="space-y-3">
            <button
              onClick={() => {
                setVoidMode(true);
                setVoidEntryTime(Date.now());
              }}
              className="flex items-center gap-2 px-3 py-2 rounded bg-purple-900/30 text-purple-300 hover:bg-purple-900/50 transition-all w-full border border-purple-500/20"
            >
              <Moon className="w-4 h-4" />
              Enter Room 64
              <span className="text-xs opacity-60 ml-auto">V</span>
            </button>

            <button
              onClick={() => setIsObserving(!isObserving)}
              className={`flex items-center gap-2 px-3 py-2 rounded transition-all w-full ${
                isObserving
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-800 text-blue-300 hover:bg-slate-700'
              }`}
            >
              {isObserving ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
              {isObserving ? 'Observing' : 'Flowing'}
              <span className="text-xs opacity-60 ml-auto">O</span>
            </button>

            <button
              onClick={releaseAll}
              className="flex items-center gap-2 px-3 py-2 rounded bg-purple-600/20 text-purple-300 hover:bg-purple-600/30 transition-all w-full"
            >
              <Waves className="w-4 h-4" />
              Release All
              <span className="text-xs opacity-60 ml-auto">R</span>
            </button>

            <button
              onClick={() => setIsPaused(!isPaused)}
              className={`flex items-center gap-2 px-3 py-2 rounded transition-all w-full ${
                isPaused
                  ? 'bg-orange-600/20 text-orange-300'
                  : 'bg-slate-800 text-blue-300 hover:bg-slate-700'
              }`}
            >
              {isPaused ? <Play className="w-4 h-4" /> : <Pause className="w-4 h-4" />}
              {isPaused ? 'Paused' : 'Playing'}
              <span className="text-xs opacity-60 ml-auto">Space</span>
            </button>

            <div className="flex gap-2">
              <button
                onClick={() => setShowConnections(!showConnections)}
                className={`flex-1 px-2 py-1 rounded text-xs transition-all ${
                  showConnections
                    ? 'bg-cyan-600/20 text-cyan-300'
                    : 'bg-slate-800 text-slate-400'
                }`}
                title="Toggle Connections (C)"
              >
                Connections
              </button>
              <button
                onClick={() => setShowWaves(!showWaves)}
                className={`flex-1 px-2 py-1 rounded text-xs transition-all ${
                  showWaves
                    ? 'bg-purple-600/20 text-purple-300'
                    : 'bg-slate-800 text-slate-400'
                }`}
                title="Toggle Waves (W)"
              >
                Waves
              </button>
            </div>

            <div>
              <label className="text-cyan-300 text-xs font-mono">Resonance Field</label>
              <input
                type="range"
                min="0"
                max="2"
                step="0.1"
                value={resonanceLevel}
                onChange={(e) => setResonanceLevel(parseFloat(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="text-purple-300 text-xs font-mono">Harmonic Mode</label>
              <select
                value={harmonicMode}
                onChange={(e) => setHarmonicMode(e.target.value)}
                className="w-full bg-slate-800 text-blue-300 rounded px-2 py-1 text-xs"
              >
                <option value="individual">Individual</option>
                <option value="collective">Collective</option>
              </select>
            </div>

            <div>
              <label className="text-pink-300 text-xs font-mono">Pattern (1/2)</label>
              <select
                value={crystalPattern}
                onChange={(e) => setCrystalPattern(e.target.value)}
                className="w-full bg-slate-800 text-blue-300 rounded px-2 py-1 text-xs"
              >
                <option value="free">Free Flow</option>
                <option value="sacred">Sacred Geometry</option>
              </select>
            </div>

            {/* LIMNUS Depth Layer Controls */}
            <div className="pt-3 border-t border-blue-500/20">
              <label className="text-cyan-300 text-xs font-mono mb-2 block">
                🌀 LIMNUS Depth Layers (0-5)
              </label>
              <div className="grid grid-cols-3 gap-1">
                {[0, 1, 2, 3, 4, 5].map(depth => (
                  <button
                    key={depth}
                    onClick={() => toggleDepth(depth)}
                    className={`px-2 py-1 rounded text-xs transition-all ${
                      activeDepths.has(depth)
                        ? 'bg-blue-600/30 text-blue-300 border border-blue-400/30'
                        : 'bg-slate-800 text-slate-500 border border-slate-700'
                    }`}
                    title={`Toggle Depth ${depth} (press ${depth})`}
                  >
                    D{depth}
                  </button>
                ))}
              </div>
              <p className="text-xs text-slate-400 mt-2">
                {memories.filter(m => activeDepths.has(m.limnusDepth)).length} / {memories.length} active
              </p>
            </div>
          </div>

          {/* Coherence Meter */}
          <div className="mt-4 pt-3 border-t border-blue-500/20">
            <div className="flex items-center justify-between mb-1">
              <span className="text-cyan-300 text-xs font-mono">Global Coherence</span>
              <span className="text-cyan-400 text-xs">{(globalCoherence * 100).toFixed(1)}%</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-blue-500 to-cyan-400 h-2 rounded-full transition-all duration-500"
                style={{ width: `${globalCoherence * 100}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Status Display - Hidden in Void Mode */}
      {!voidMode && selectedMemory !== null && memories[selectedMemory] && (
        <div
          className={`absolute top-20 right-4 z-20 bg-slate-900/80 backdrop-blur p-4 rounded-lg border border-cyan-500/20 transition-all duration-300 ${
            uiVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-4 pointer-events-none'
          }`}
        >
          <p className="text-cyan-300 font-mono text-sm">
            Memory #{selectedMemory} crystallized
          </p>
          <p className="text-cyan-400/60 text-xs mt-1">
            {memories[selectedMemory].content}
          </p>
          <p className="text-purple-400/60 text-xs">
            Archetype: {memories[selectedMemory].archetype}
          </p>
          <p className="text-pink-400/60 text-xs">
            Harmonic: {memories[selectedMemory].harmonic}Hz
          </p>
          <p className="text-blue-400/60 text-xs">
            Depth Layer: {memories[selectedMemory].limnusDepth}
          </p>

          {/* Helix State Display */}
          <div className="mt-2 pt-2 border-t border-cyan-500/10">
            <p className="text-cyan-300/80 text-xs font-mono mb-1">Helix State (θ, z, r)</p>
            <p className="text-xs text-blue-300/60">
              θ: {memories[selectedMemory].helixState.theta.toFixed(3)} rad
            </p>
            <p className="text-xs text-purple-300/60">
              z: {memories[selectedMemory].helixState.z.toFixed(3)}
            </p>
            <p className="text-xs text-pink-300/60">
              r: {memories[selectedMemory].helixState.r.toFixed(3)}
            </p>
          </div>

          <div className="mt-2">
            <span className="text-blue-300/60 text-xs">Coherence</span>
            <div className="w-full bg-slate-800 rounded-full h-1 mt-1">
              <div
                className="bg-gradient-to-r from-purple-500 to-pink-400 h-1 rounded-full transition-all"
                style={{ width: `${memories[selectedMemory].coherenceLevel * 100}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Rotation Mode Helper - Hidden in Void Mode */}
      {!voidMode && modifierPressed && !isDragging && (rotation.x === 0 && rotation.y === 0) && (
        <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 z-10 pointer-events-none">
          <div className="text-cyan-400/60 font-mono text-xs bg-slate-900/70 px-3 py-1 rounded-full backdrop-blur animate-pulse">
            Drag to rotate view
          </div>
        </div>
      )}

      {/* Drag Mode Indicator - Hidden in Void Mode */}
      {!voidMode && isDragging && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-30 pointer-events-none">
          <div className="text-cyan-400/60 font-mono text-sm animate-pulse">
            Rotating...
          </div>
        </div>
      )}

      {/* Rotation Indicator - Hidden in Void Mode */}
      {!voidMode && (rotation.x !== 0 || rotation.y !== 0) && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-10 pointer-events-none">
          <div className="text-blue-400/40 font-mono text-xs bg-slate-900/50 px-3 py-1 rounded-full backdrop-blur">
            Rotation: X:{rotation.x.toFixed(0)}° Y:{rotation.y.toFixed(0)}°
            <button
              onClick={() => setRotation({ x: 0, y: 0 })}
              className="ml-2 text-cyan-300 hover:text-cyan-100 pointer-events-auto"
              title="Double-click anywhere to reset"
            >
              Reset
            </button>
          </div>
        </div>
      )}

      {/* Pause Indicator - Hidden in Void Mode */}
      {!voidMode && isPaused && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 pointer-events-none">
          <div className="text-blue-400/30 font-mono text-2xl animate-pulse">
            PAUSED
          </div>
        </div>
      )}

      {/* Canvas for wave patterns and helical connections */}
      <canvas
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight}
        className="absolute inset-0 z-0"
      />

      {/* Memory particles */}
      <div
        className="absolute inset-0 z-10"
        style={{
          transform: `perspective(1000px) rotateX(${rotation.x}deg) rotateY(${rotation.y}deg)`,
          transformStyle: 'preserve-3d',
          transition: isDragging ? 'none' : 'transform 0.3s ease-out'
        }}
      >
        {memories.map(memory => {
          const transformed = transformCoordinates(memory.x, memory.y, memory.crystallized ? 20 : 0);
          const isActive = activeDepths.has(memory.limnusDepth);

          return (
            <div
              key={memory.id}
              onClick={(e) => {
                e.stopPropagation();
                handleObservation(memory.id);
              }}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 transition-all cursor-pointer ${
                memory.crystallized ? 'duration-500' : 'duration-100'
              }`}
              style={{
                left: `${transformed.x}%`,
                top: `${transformed.y}%`,
                width: (memory.crystallized ? memory.size * 2 : memory.size) * transformed.scale,
                height: (memory.crystallized ? memory.size * 2 : memory.size) * transformed.scale,
                zIndex: Math.round(transformed.z + 100),
                opacity: isActive ? 0.5 + transformed.scale * 0.5 : 0.1
              }}
            >
              <div
                className={`w-full h-full rounded-full flex items-center justify-center relative ${
                  memory.crystallized
                    ? voidMode
                      ? 'bg-gradient-to-br from-purple-400 to-purple-600'
                      : 'bg-gradient-to-br from-cyan-400 to-blue-600'
                    : voidMode
                    ? 'bg-gradient-to-br from-purple-500/20 to-purple-600/20'
                    : 'bg-gradient-to-br from-blue-500/30 to-purple-500/30'
                }`}
                style={{
                  boxShadow: memory.crystallized
                    ? voidMode
                      ? `0 0 ${20 + memory.coherenceLevel * 30}px rgba(147, 112, 219, 0.8)`
                      : `0 0 ${20 + memory.coherenceLevel * 30}px ${memory.color}`
                    : 'none',
                  filter: memory.crystallized
                    ? `brightness(${1 + memory.coherenceLevel * 0.5})`
                    : voidMode
                    ? 'blur(1px)'
                    : 'blur(0.5px)',
                  transform: memory.crystallized
                    ? `rotate(${wavePhase * memory.harmonic * 0.1}deg) scale(${1 + memory.coherenceLevel * 0.2})`
                    : `scale(${1 + Math.sin(wavePhase + memory.phase) * 0.1})`,
                }}
              >
                {memory.crystallized && (
                  <>
                    {/* Inner crystal structure */}
                    <div
                      className="absolute inset-2 border border-white/20 rounded-full"
                      style={{
                        transform: `rotate(${-wavePhase * memory.harmonic * 0.05}deg)`,
                      }}
                    />
                    <div
                      className="absolute inset-3 border border-white/10 rounded-full"
                      style={{
                        transform: `rotate(${wavePhase * memory.harmonic * 0.03}deg)`,
                      }}
                    />
                    {/* Content */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-white text-xs font-mono opacity-90 text-center">
                        {memory.content}
                      </span>
                    </div>
                  </>
                )}
              </div>

              {/* Multi-layered resonance ripples */}
              {memory.crystallized && (
                <>
                  <div
                    className="absolute inset-0 rounded-full border animate-ping"
                    style={{
                      borderColor: memory.color,
                      opacity: 0.3 * memory.coherenceLevel,
                    }}
                  />
                  <div
                    className="absolute inset-0 rounded-full border animate-ping"
                    style={{
                      borderColor: memory.color,
                      opacity: 0.2 * memory.coherenceLevel,
                      animationDelay: '200ms',
                    }}
                  />
                  <div
                    className="absolute inset-0 rounded-full border animate-ping"
                    style={{
                      borderColor: memory.color,
                      opacity: 0.1 * memory.coherenceLevel,
                      animationDelay: '400ms',
                    }}
                  />
                </>
              )}
            </div>
          );
        })}
      </div>

      {/* Keyboard Shortcuts Panel - Hidden in Void Mode */}
      {!voidMode && (
        <div
          className={`absolute bottom-4 right-4 z-20 transition-all duration-300 ${
            showShortcuts
              ? 'opacity-100 translate-y-0 scale-100'
              : 'opacity-0 translate-y-4 scale-95 pointer-events-none'
          }`}
        >
          <div className="bg-slate-900/95 backdrop-blur-md p-4 rounded-lg border border-purple-500/20 shadow-xl shadow-purple-900/30 w-80">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-purple-300 font-mono text-sm flex items-center gap-2">
                <Keyboard className="w-4 h-4" />
                Keyboard Shortcuts
              </h3>
              <button
                onClick={() => setShowShortcuts(false)}
                className="text-purple-400/60 hover:text-purple-300 transition-colors"
                title="Close (or press ?)"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-x-6 gap-y-1 text-xs">
              <div className="space-y-1">
                <p className="text-cyan-400 font-bold mb-1 border-b border-cyan-500/20 pb-1">View</p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Toggle UI</span>
                  <span className="text-blue-300 font-mono ml-2">H</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Interactions</span>
                  <span className="text-blue-300 font-mono ml-2">I</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Pause/Play</span>
                  <span className="text-blue-300 font-mono ml-2">Space</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Connections</span>
                  <span className="text-blue-300 font-mono ml-2">C</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Wave Field</span>
                  <span className="text-blue-300 font-mono ml-2">W</span>
                </p>
              </div>

              <div className="space-y-1">
                <p className="text-purple-400 font-bold mb-1 border-b border-purple-500/20 pb-1">Actions</p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Observe</span>
                  <span className="text-blue-300 font-mono ml-2">O</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Release All</span>
                  <span className="text-blue-300 font-mono ml-2">R</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Free Flow</span>
                  <span className="text-blue-300 font-mono ml-2">1</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Sacred</span>
                  <span className="text-blue-300 font-mono ml-2">2</span>
                </p>
                <p className="flex justify-between">
                  <span className="text-purple-300/80">Void Mode</span>
                  <span className="text-blue-300 font-mono ml-2">V</span>
                </p>
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-purple-500/20 space-y-1 text-xs">
              <p className="text-pink-400 font-bold mb-1">LIMNUS Depth Layers</p>
              <div className="space-y-1 text-purple-300/80">
                <p className="flex justify-between">
                  <span>Toggle depths 0-5</span>
                  <span className="text-blue-300 font-mono text-xs">0-5 keys</span>
                </p>
                <p className="text-purple-400/60 text-xs">
                  Depth 5 isolated (boundary layer)
                </p>
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-purple-500/20 space-y-1 text-xs">
              <p className="text-pink-400 font-bold mb-1">3D Controls</p>
              <div className="space-y-1 text-purple-300/80">
                <p className="flex justify-between">
                  <span>Rotate view</span>
                  <span className="text-blue-300 font-mono text-xs">Shift/Ctrl + Drag</span>
                </p>
                <p className="flex justify-between">
                  <span>Reset rotation</span>
                  <span className="text-blue-300 font-mono text-xs">Double-click / ESC</span>
                </p>
                <p className="flex justify-between">
                  <span>Create pulse</span>
                  <span className="text-blue-300 font-mono text-xs">Click empty space</span>
                </p>
              </div>
            </div>

            <div className="mt-3 pt-2 border-t border-purple-500/10 text-purple-400/50 text-xs text-center">
              Press <span className="font-mono bg-purple-900/30 px-1.5 py-0.5 rounded text-purple-300">?</span> to toggle
            </div>
          </div>
        </div>
      )}

      {/* Enhanced Instructions - Hidden in Void Mode */}
      {!voidMode && (
        <div
          className={`absolute bottom-4 left-4 z-20 transition-all duration-300 ${
            showInteractions
              ? 'opacity-100 translate-y-0 scale-100'
              : 'opacity-0 translate-y-4 scale-95 pointer-events-none'
          }`}
        >
          <div className="bg-slate-900/95 backdrop-blur-md p-3 rounded-lg border border-cyan-500/20 shadow-lg shadow-cyan-900/20 max-w-xs">
            <div className="flex items-center justify-between mb-2">
              <p className="text-cyan-400 font-bold text-sm flex items-center gap-2">
                <Info className="w-4 h-4" />
                How to Interact
              </p>
              <button
                onClick={() => setShowInteractions(false)}
                className="text-cyan-400/60 hover:text-cyan-300 transition-colors"
                title="Close (or press I)"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex items-start gap-2">
                <Activity className="w-3 h-3 text-blue-400 mt-0.5 flex-shrink-0" />
                <span className="text-blue-300/80">Click empty space to create force pulses</span>
              </div>
              <div className="flex items-start gap-2">
                <Eye className="w-3 h-3 text-cyan-400 mt-0.5 flex-shrink-0" />
                <span className="text-blue-300/80">Click memories while observing to crystallize</span>
              </div>
              <div className="flex items-start gap-2">
                <Circle className="w-3 h-3 text-purple-400 mt-0.5 flex-shrink-0" />
                <span className="text-blue-300/80">Shift/Ctrl + drag to rotate view</span>
              </div>
              <div className="flex items-start gap-2">
                <Zap className="w-3 h-3 text-yellow-400 mt-0.5 flex-shrink-0" />
                <span className="text-blue-300/80">Helical magnetic field connections</span>
              </div>
              <div className="flex items-start gap-2">
                <Heart className="w-3 h-3 text-pink-400 mt-0.5 flex-shrink-0" />
                <span className="text-blue-300/80">Helix (θ, z, r) evolves with crystallization</span>
              </div>
            </div>

            <div className="mt-3 pt-2 border-t border-cyan-500/10 text-cyan-400/50 text-xs text-center">
              Press <span className="font-mono bg-cyan-900/30 px-1.5 py-0.5 rounded text-cyan-300">I</span> to toggle
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CrystalMemoryField;
