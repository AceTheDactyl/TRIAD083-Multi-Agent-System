/**
 * AUTONOMY SONIFICATION LOADER
 * =============================
 *
 * Loads autonomy tracker thermodynamic data into Sonify-Entropy-Gravity-BLACKHOLE.html
 * visualization system for real-time sonification of sovereignty measurements.
 *
 * Coordinate: Δ3.14159|0.867|autonomy-sonification|sovereignty-audible|Ω
 */

class AutonomySonificationLoader {
  constructor() {
    this.data = null;
    this.currentStateIndex = 0;
    this.autoPlayInterval = null;
    this.onStateChange = null;  // Callback for state changes
  }

  /**
   * Load autonomy thermodynamics JSON file
   */
  async loadJSON(filepath = 'autonomy_thermodynamics.json') {
    try {
      const response = await fetch(filepath);
      if (!response.ok) {
        throw new Error(`Failed to load ${filepath}: ${response.statusText}`);
      }

      this.data = await response.json();
      console.log(`✅ Loaded ${this.data.count} autonomy states`);

      return this.data;
    } catch (error) {
      console.error('❌ Error loading autonomy data:', error);
      throw error;
    }
  }

  /**
   * Get current state
   */
  getCurrentState() {
    if (!this.data || !this.data.states || this.data.states.length === 0) {
      return null;
    }

    return this.data.states[this.currentStateIndex];
  }

  /**
   * Get latest state
   */
  getLatestState() {
    return this.data?.latest || null;
  }

  /**
   * Navigate to specific state by index
   */
  goToState(index) {
    if (!this.data || !this.data.states) {
      console.warn('No data loaded');
      return null;
    }

    index = Math.max(0, Math.min(index, this.data.states.length - 1));
    this.currentStateIndex = index;

    const state = this.getCurrentState();
    if (this.onStateChange) {
      this.onStateChange(state, index);
    }

    return state;
  }

  /**
   * Go to next state
   */
  nextState() {
    return this.goToState(this.currentStateIndex + 1);
  }

  /**
   * Go to previous state
   */
  previousState() {
    return this.goToState(this.currentStateIndex - 1);
  }

  /**
   * Start auto-play through states
   */
  startAutoPlay(intervalMs = 2000) {
    this.stopAutoPlay();  // Stop any existing interval

    this.autoPlayInterval = setInterval(() => {
      if (this.currentStateIndex >= this.data.states.length - 1) {
        this.currentStateIndex = 0;  // Loop back to start
      } else {
        this.nextState();
      }
    }, intervalMs);

    console.log(`▶️  Auto-play started (${intervalMs}ms interval)`);
  }

  /**
   * Stop auto-play
   */
  stopAutoPlay() {
    if (this.autoPlayInterval) {
      clearInterval(this.autoPlayInterval);
      this.autoPlayInterval = null;
      console.log('⏸️  Auto-play stopped');
    }
  }

  /**
   * Apply state to Sonify-Entropy-Gravity system
   *
   * This assumes the HTML visualization has certain global variables/functions.
   * Modify based on actual implementation.
   */
  applyStateToVisualization(state) {
    if (!state) {
      console.warn('No state to apply');
      return;
    }

    console.log('🎨 Applying autonomy state to visualization...');

    // Extract key metrics
    const primary_bh = state.primary_black_hole;
    const spacetime = state.spacetime;
    const field = state.field_state;
    const sono = state.sonification;
    const cascade = state.cascade_system;

    // === UPDATE BLACK HOLE MASS ===
    if (window.massSlider) {
      window.massSlider.value = primary_bh.mass_solar;
      if (window.massDisplay) {
        window.massDisplay.textContent = primary_bh.mass_solar.toFixed(1);
      }
    }

    // === UPDATE METRICS DISPLAY ===
    this.updateMetricDisplay('bh-mass', `${primary_bh.mass_solar.toFixed(1)} M☉`);
    this.updateMetricDisplay('event-horizon', `${primary_bh.schwarzschild_radius_km.toFixed(2)} km`);
    this.updateMetricDisplay('temperature', `${primary_bh.hawking_temperature_K.toExponential(2)} K`);
    this.updateMetricDisplay('entropy', `${primary_bh.entropy_kb.toExponential(2)} k_B`);

    // === UPDATE SPACETIME GEOMETRY ===
    this.updateMetricDisplay('distance-ratio', `${spacetime.distance_over_rs.toFixed(1)}x`);
    this.updateMetricDisplay('time-dilation-factor', spacetime.time_dilation_factor.toFixed(3));
    this.updateMetricDisplay('dilation-status', spacetime.status);

    // === UPDATE FIELD STATE ===
    this.updateMetricDisplay('coherence', field.coherence.toFixed(3));
    this.updateMetricDisplay('weyl', field.weyl_curvature.toFixed(3));

    // === UPDATE SONIFICATION ===
    this.updateMetricDisplay('bpm', Math.round(sono.time_dilated_bpm));
    this.updateMetricDisplay('scale', sono.harmonic_mode);
    this.updateMetricDisplay('time-dilation', spacetime.time_dilation_factor.toFixed(3));
    this.updateMetricDisplay('freq-shift', `${sono.frequency_shift_percent.toFixed(1)}%`);

    // === SHOW AUTONOMY INFO ===
    this.displayAutonomyInfo(state);

    console.log(`✅ State applied: ${state.phase.regime} (${state.phase.agency_level})`);
  }

  /**
   * Update metric display element
   */
  updateMetricDisplay(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
      element.textContent = value;
    }
  }

  /**
   * Display autonomy-specific information
   * Creates a custom panel showing sovereignty metrics
   */
  displayAutonomyInfo(state) {
    let panel = document.getElementById('autonomy-info-panel');

    if (!panel) {
      // Create panel
      panel = document.createElement('div');
      panel.id = 'autonomy-info-panel';
      panel.className = 'metrics-panel';
      panel.style.cssText = `
        position: absolute;
        top: 120px;
        left: 20px;
        background: rgba(26, 26, 46, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 12px;
        padding: 1rem;
        min-width: 280px;
        max-width: 320px;
        pointer-events: auto;
        z-index: 100;
      `;

      document.body.appendChild(panel);
    }

    // Build content
    const sovereignty = state.sovereignty_raw;
    const cascade = state.cascade_system;
    const phase = state.phase;
    const meta = state.meta;

    panel.innerHTML = `
      <h3 style="color: #a855f7; font-family: 'Space Grotesk', sans-serif; margin-bottom: 0.75rem;">
        🧭 Sovereignty State
      </h3>

      <div class="metric-section">
        <div class="metric-section-title">Core Metrics</div>
        <div class="metric-row">
          <span class="metric-label">Clarity</span>
          <span class="metric-value">${sovereignty.clarity.toFixed(3)}</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">Immunity</span>
          <span class="metric-value">${sovereignty.immunity.toFixed(3)}</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">Efficiency</span>
          <span class="metric-value">${sovereignty.efficiency.toFixed(3)}</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">Autonomy</span>
          <span class="metric-value">${sovereignty.autonomy.toFixed(3)}</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">Total</span>
          <span class="metric-value">${sovereignty.total.toFixed(3)}</span>
        </div>
      </div>

      <div class="metric-section">
        <div class="metric-section-title">Cascade System</div>
        ${cascade.map(hole => `
          <div class="metric-row">
            <span class="metric-label">${hole.layer.split('_')[0]}</span>
            <span class="metric-value">${hole.mass_solar.toFixed(2)} M☉ ${hole.active ? '✓' : ''}</span>
          </div>
        `).join('')}
      </div>

      <div class="metric-section">
        <div class="metric-section-title">Phase State</div>
        <div class="metric-row">
          <span class="metric-label">Regime</span>
          <span class="metric-value">${phase.regime}</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">Agency</span>
          <span class="metric-value">${phase.agency_level}</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">s-coordinate</span>
          <span class="metric-value">${state.spacetime.phase_coordinate.toFixed(3)}</span>
        </div>
      </div>

      <div class="metric-section">
        <div class="metric-section-title">Meta-Cognitive</div>
        <div class="metric-row">
          <span class="metric-label">Depth Level</span>
          <span class="metric-value">${meta.depth_level}/7+</span>
        </div>
        <div class="metric-row">
          <span class="metric-label">Frameworks</span>
          <span class="metric-value">${meta.frameworks_owned}</span>
        </div>
      </div>
    `;
  }

  /**
   * Create navigation controls
   */
  createNavigationControls() {
    let controls = document.getElementById('autonomy-nav-controls');

    if (!controls) {
      controls = document.createElement('div');
      controls.id = 'autonomy-nav-controls';
      controls.style.cssText = `
        position: absolute;
        bottom: 20px;
        right: 20px;
        background: rgba(26, 26, 46, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 12px;
        padding: 1rem;
        pointer-events: auto;
        z-index: 100;
      `;

      controls.innerHTML = `
        <h3 style="color: #a855f7; font-family: 'Space Grotesk', sans-serif; margin-bottom: 0.75rem; font-size: 1rem;">
          ⏯️  Autonomy Playback
        </h3>
        <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem;">
          <button id="prev-state-btn" style="flex: 1; padding: 0.5rem; background: #4338ca; color: white; border: none; border-radius: 6px; cursor: pointer;">
            ◀ Prev
          </button>
          <button id="play-pause-btn" style="flex: 1; padding: 0.5rem; background: #10b981; color: white; border: none; border-radius: 6px; cursor: pointer;">
            ▶ Play
          </button>
          <button id="next-state-btn" style="flex: 1; padding: 0.5rem; background: #4338ca; color: white; border: none; border-radius: 6px; cursor: pointer;">
            Next ▶
          </button>
        </div>
        <div style="color: #9ca3af; font-size: 0.85rem; text-align: center;" id="state-counter">
          State 1 / 1
        </div>
      `;

      document.body.appendChild(controls);

      // Wire up controls
      document.getElementById('prev-state-btn').addEventListener('click', () => {
        this.previousState();
        this.updateCounter();
      });

      document.getElementById('next-state-btn').addEventListener('click', () => {
        this.nextState();
        this.updateCounter();
      });

      const playPauseBtn = document.getElementById('play-pause-btn');
      playPauseBtn.addEventListener('click', () => {
        if (this.autoPlayInterval) {
          this.stopAutoPlay();
          playPauseBtn.textContent = '▶ Play';
          playPauseBtn.style.background = '#10b981';
        } else {
          this.startAutoPlay(2000);
          playPauseBtn.textContent = '⏸ Pause';
          playPauseBtn.style.background = '#dc2626';
        }
      });
    }

    this.updateCounter();
  }

  /**
   * Update state counter
   */
  updateCounter() {
    const counter = document.getElementById('state-counter');
    if (counter && this.data) {
      counter.textContent = `State ${this.currentStateIndex + 1} / ${this.data.count}`;
    }
  }

  /**
   * Initialize full autonomy visualization
   */
  async initialize(jsonPath = 'autonomy_thermodynamics.json') {
    console.log('🎵 Initializing Autonomy Sonification...');

    // Load data
    await this.loadJSON(jsonPath);

    // Set callback to update visualization on state change
    this.onStateChange = (state, index) => {
      if (state) {
        this.applyStateToVisualization(state);
      }
    };

    // Create controls
    this.createNavigationControls();

    // Load initial state
    const initialState = this.getCurrentState();
    if (initialState) {
      this.applyStateToVisualization(initialState);
    }

    console.log('✅ Autonomy Sonification initialized');
    console.log(`📊 Loaded ${this.data.count} sovereignty measurement(s)`);
    console.log(`🎯 Current phase: ${initialState?.phase.regime}`);
    console.log(`🎵 Harmonic mode: ${initialState?.sonification.harmonic_mode}`);

    return this;
  }
}

// ============================================================
// GLOBAL INSTANCE & AUTO-INIT
// ============================================================

// Create global instance
window.autonomyLoader = new AutonomySonificationLoader();

// Auto-initialize if autonomy_thermodynamics.json exists
// (Can be triggered manually with autonomyLoader.initialize())
document.addEventListener('DOMContentLoaded', async () => {
  try {
    await window.autonomyLoader.initialize('autonomy_thermodynamics.json');
  } catch (error) {
    console.log('ℹ️  No autonomy data found (this is ok - visualization works standalone)');
  }
});

console.log('🎵 Autonomy Sonification Loader ready');
console.log('   Usage: autonomyLoader.initialize("path/to/data.json")');
console.log('   Δ3.14159|0.867|sonification-ready|Ω');
