# Enhanced Monitoring Tools

Advanced monitoring capabilities that go beyond basic system checks.

## Tools

### Core Monitoring
- `system-health-dashboard.py` - Comprehensive system health with visual dashboard
- `multi-service-monitor.py` - Monitor multiple services with dependency tracking
- `alert-manager.py` - Intelligent alert system with smart thresholds
- `log-analyzer.py` - Log analysis with pattern detection and anomaly alerts

### Specialized Monitors
- `network-monitor.py` - Network performance and connectivity monitoring
- `resource-monitor.py` - Deep dive into CPU, memory, disk, and GPU usage
- `process-monitor.py` - Process lifecycle and performance tracking
- `security-monitor.py` - Security event monitoring and threat detection

### Dashboard & Reporting
- `monitoring-dashboard.py` - Web-based monitoring dashboard
- `report-generator.py` - Automated monitoring reports
- `alert-digest.py` - Daily/weekly alert summaries

## Configuration

All monitors use the centralized config at `../config/monitoring-config.yaml`

## Integration

- Slack/Discord/Telegram notifications
- Email alerts for critical issues
- Integration with existing heartbeat system
- API endpoints for external systems