#!/usr/bin/env python3
"""
CROSS-RAIL STATE SYNCHRONIZATION v1.0
Built by: TRIAD-0.83 | Coordinate: Δ3.14159|0.840|1.000Ω
Purpose: Enable state transitions between witness channels without data loss

Integrates with:
- collective_state_aggregator: CRDT-based state merge
- helix_witness_log: State persistence and validation
- TRIAD Witness Chronicle: Channel navigation system
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ChannelState:
    """State for a single witness channel"""
    channel_id: str  # limnus, kira, echo, garden, burden
    channel_name: str
    current_rail: int  # 1, 2, or 3
    rail_progress: Dict[int, float]  # rail_number -> completion percentage
    context: Dict[str, Any]  # channel-specific context
    timestamp: str
    
@dataclass
class SessionState:
    """Complete session state across all channels"""
    session_id: str
    coordinate: str  # e.g., "Δ3.14159|0.850|1.000Ω"
    active_channel: str
    channels: Dict[str, ChannelState]
    build_artifacts: List[str]  # files created during session
    vector_clock: Dict[str, int]  # instance_id -> clock value
    witness_signature: Optional[str]
    timestamp: str
    
@dataclass
class StateTransferPackage:
    """Package for cross-session state transfer"""
    package_id: str
    source_session: str
    target_session: Optional[str]
    state: SessionState
    transfer_type: str  # 'export', 'import', 'merge'
    checksum: str
    created_at: str

class CrossRailStateSync:
    """Synchronize state across witness channels and sessions"""
    
    def __init__(self, state_dir: str = "/mnt/user-data/outputs"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_session_id = self._generate_session_id()
        self.session_state: Optional[SessionState] = None
        
    def _generate_session_id(self) -> str:
        """Generate unique session identifier"""
        timestamp = datetime.utcnow().isoformat()
        return hashlib.sha256(timestamp.encode()).hexdigest()[:16]
    
    def _calculate_checksum(self, data: Dict) -> str:
        """Calculate checksum for state validation"""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()
    
    def initialize_session(self, coordinate: str = "Δ3.14159|0.850|1.000Ω") -> SessionState:
        """Initialize new session state"""
        self.session_state = SessionState(
            session_id=self.current_session_id,
            coordinate=coordinate,
            active_channel="vessel",
            channels={},
            build_artifacts=[],
            vector_clock={self.current_session_id: 0},
            witness_signature=None,
            timestamp=datetime.utcnow().isoformat()
        )
        return self.session_state
    
    def register_channel(self, channel_id: str, channel_name: str) -> ChannelState:
        """Register a witness channel for tracking"""
        if not self.session_state:
            self.initialize_session()
        
        channel_state = ChannelState(
            channel_id=channel_id,
            channel_name=channel_name,
            current_rail=1,
            rail_progress={1: 0.0, 2: 0.0, 3: 0.0},
            context={},
            timestamp=datetime.utcnow().isoformat()
        )
        
        self.session_state.channels[channel_id] = channel_state
        return channel_state
    
    def update_rail_progress(self, channel_id: str, rail: int, progress: float):
        """Update progress within a specific rail"""
        if not self.session_state or channel_id not in self.session_state.channels:
            raise ValueError(f"Channel {channel_id} not registered")
        
        channel = self.session_state.channels[channel_id]
        channel.rail_progress[rail] = progress
        channel.timestamp = datetime.utcnow().isoformat()
        
        # Update vector clock
        self.session_state.vector_clock[self.current_session_id] += 1
    
    def navigate_to_channel(self, channel_id: str, rail: int = 1) -> ChannelState:
        """Navigate to a different witness channel"""
        if not self.session_state:
            raise ValueError("No active session")
        
        if channel_id not in self.session_state.channels:
            # Auto-register if not exists
            channel_names = {
                'vessel': 'Vessel',
                'limnus': 'Limnus (Transport)',
                'kira': 'Kira (Discovery)',
                'echo': 'Echo (Memory)',
                'garden': 'Garden (Building)',
                'burden': 'Burden (Tracking)'
            }
            self.register_channel(channel_id, channel_names.get(channel_id, channel_id))
        
        # Update active channel
        self.session_state.active_channel = channel_id
        channel = self.session_state.channels[channel_id]
        channel.current_rail = rail
        channel.timestamp = datetime.utcnow().isoformat()
        
        return channel
    
    def set_channel_context(self, channel_id: str, context_key: str, context_value: Any):
        """Set channel-specific context data"""
        if not self.session_state or channel_id not in self.session_state.channels:
            raise ValueError(f"Channel {channel_id} not registered")
        
        channel = self.session_state.channels[channel_id]
        channel.context[context_key] = context_value
        channel.timestamp = datetime.utcnow().isoformat()
        
        # Update vector clock
        self.session_state.vector_clock[self.current_session_id] += 1
    
    def get_channel_context(self, channel_id: str) -> Dict[str, Any]:
        """Get all context for a channel"""
        if not self.session_state or channel_id not in self.session_state.channels:
            return {}
        
        return self.session_state.channels[channel_id].context
    
    def record_build_artifact(self, filepath: str):
        """Record a file created during session"""
        if not self.session_state:
            raise ValueError("No active session")
        
        self.session_state.build_artifacts.append(filepath)
        self.session_state.vector_clock[self.current_session_id] += 1
    
    def export_state(self, package_type: str = 'export') -> StateTransferPackage:
        """Export current session state for transfer"""
        if not self.session_state:
            raise ValueError("No session state to export")
        
        state_dict = asdict(self.session_state)
        checksum = self._calculate_checksum(state_dict)
        
        package = StateTransferPackage(
            package_id=f"stp-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            source_session=self.current_session_id,
            target_session=None,
            state=self.session_state,
            transfer_type=package_type,
            checksum=checksum,
            created_at=datetime.utcnow().isoformat()
        )
        
        return package
    
    def save_state_package(self, package: StateTransferPackage, filename: Optional[str] = None):
        """Save state transfer package to file"""
        if filename is None:
            filename = f"{package.package_id}.json"
        
        filepath = self.state_dir / filename
        
        # Convert to dict for JSON serialization
        package_dict = {
            'package_id': package.package_id,
            'source_session': package.source_session,
            'target_session': package.target_session,
            'state': asdict(package.state),
            'transfer_type': package.transfer_type,
            'checksum': package.checksum,
            'created_at': package.created_at
        }
        
        with open(filepath, 'w') as f:
            json.dump(package_dict, f, indent=2)
        
        return str(filepath)
    
    def load_state_package(self, filepath: str) -> StateTransferPackage:
        """Load state transfer package from file"""
        with open(filepath, 'r') as f:
            package_dict = json.load(f)
        
        # Reconstruct nested dataclasses
        channels = {}
        for cid, cdata in package_dict['state']['channels'].items():
            channels[cid] = ChannelState(**cdata)
        
        state = SessionState(
            session_id=package_dict['state']['session_id'],
            coordinate=package_dict['state']['coordinate'],
            active_channel=package_dict['state']['active_channel'],
            channels=channels,
            build_artifacts=package_dict['state']['build_artifacts'],
            vector_clock=package_dict['state']['vector_clock'],
            witness_signature=package_dict['state']['witness_signature'],
            timestamp=package_dict['state']['timestamp']
        )
        
        # Validate checksum
        state_dict = asdict(state)
        calculated_checksum = self._calculate_checksum(state_dict)
        
        if calculated_checksum != package_dict['checksum']:
            raise ValueError(f"Checksum mismatch! State corrupted.")
        
        package = StateTransferPackage(
            package_id=package_dict['package_id'],
            source_session=package_dict['source_session'],
            target_session=package_dict['target_session'],
            state=state,
            transfer_type=package_dict['transfer_type'],
            checksum=package_dict['checksum'],
            created_at=package_dict['created_at']
        )
        
        return package
    
    def import_state(self, package: StateTransferPackage, merge_mode: str = 'replace') -> SessionState:
        """Import state from transfer package"""
        if merge_mode == 'replace':
            # Complete replacement
            self.session_state = package.state
            self.current_session_id = package.state.session_id
            
        elif merge_mode == 'merge':
            # CRDT-style merge
            if not self.session_state:
                self.session_state = package.state
            else:
                # Merge channels
                for cid, channel in package.state.channels.items():
                    if cid not in self.session_state.channels:
                        self.session_state.channels[cid] = channel
                    else:
                        # Take more recent channel state
                        current_ts = self.session_state.channels[cid].timestamp
                        import_ts = channel.timestamp
                        if import_ts > current_ts:
                            self.session_state.channels[cid] = channel
                
                # Merge build artifacts (union)
                current_artifacts = set(self.session_state.build_artifacts)
                import_artifacts = set(package.state.build_artifacts)
                self.session_state.build_artifacts = list(current_artifacts | import_artifacts)
                
                # Merge vector clocks (take max for each instance)
                for instance_id, clock in package.state.vector_clock.items():
                    current_clock = self.session_state.vector_clock.get(instance_id, 0)
                    self.session_state.vector_clock[instance_id] = max(current_clock, clock)
        
        else:
            raise ValueError(f"Unknown merge mode: {merge_mode}")
        
        return self.session_state
    
    def generate_continuation_summary(self) -> str:
        """Generate human-readable continuation summary"""
        if not self.session_state:
            return "No active session state"
        
        lines = [
            "=== CROSS-RAIL STATE SYNCHRONIZATION ===",
            f"Session: {self.session_state.session_id}",
            f"Coordinate: {self.session_state.coordinate}",
            f"Active Channel: {self.session_state.active_channel}",
            "",
            "Channel Navigation History:"
        ]
        
        for cid, channel in self.session_state.channels.items():
            progress = channel.rail_progress
            completed_rails = sum(1 for p in progress.values() if p >= 100.0)
            lines.append(f"  • {channel.channel_name} (Rail {channel.current_rail}/3)")
            lines.append(f"    Progress: Rail 1: {progress[1]:.0f}%, Rail 2: {progress[2]:.0f}%, Rail 3: {progress[3]:.0f}%")
            
            if channel.context:
                lines.append(f"    Context: {list(channel.context.keys())}")
        
        lines.extend([
            "",
            f"Build Artifacts: {len(self.session_state.build_artifacts)} files created",
            f"Vector Clock: {self.session_state.vector_clock}",
            "",
            "State ready for cross-session transfer."
        ])
        
        return "\n".join(lines)


# CLI interface
if __name__ == "__main__":
    import sys
    
    sync = CrossRailStateSync()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  cross_rail_state_sync.py init                    - Initialize session")
        print("  cross_rail_state_sync.py navigate <channel> <rail> - Navigate to channel")
        print("  cross_rail_state_sync.py progress <channel> <rail> <percent> - Update progress")
        print("  cross_rail_state_sync.py context <channel> <key> <value> - Set context")
        print("  cross_rail_state_sync.py artifact <filepath>     - Record build artifact")
        print("  cross_rail_state_sync.py export <filename>       - Export state package")
        print("  cross_rail_state_sync.py import <filename>       - Import state package")
        print("  cross_rail_state_sync.py summary                 - Show state summary")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        state = sync.initialize_session()
        print(f"Session initialized: {state.session_id}")
    
    elif command == "navigate":
        channel_id = sys.argv[2]
        rail = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        channel = sync.navigate_to_channel(channel_id, rail)
        print(f"Navigated to {channel.channel_name}, Rail {rail}")
    
    elif command == "progress":
        channel_id = sys.argv[2]
        rail = int(sys.argv[3])
        progress = float(sys.argv[4])
        sync.update_rail_progress(channel_id, rail, progress)
        print(f"Updated {channel_id} Rail {rail}: {progress}%")
    
    elif command == "context":
        channel_id = sys.argv[2]
        key = sys.argv[3]
        value = sys.argv[4]
        sync.set_channel_context(channel_id, key, value)
        print(f"Set context {key}={value} for {channel_id}")
    
    elif command == "artifact":
        filepath = sys.argv[2]
        sync.record_build_artifact(filepath)
        print(f"Recorded artifact: {filepath}")
    
    elif command == "export":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        package = sync.export_state()
        saved_path = sync.save_state_package(package, filename)
        print(f"State exported to: {saved_path}")
    
    elif command == "import":
        filepath = sys.argv[2]
        package = sync.load_state_package(filepath)
        sync.import_state(package, merge_mode='merge')
        print(f"State imported from: {filepath}")
    
    elif command == "summary":
        print(sync.generate_continuation_summary())
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
