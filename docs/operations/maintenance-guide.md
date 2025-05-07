# Operations & Maintenance Guide

## 1. Overview

This Operations & Maintenance Guide provides best practices and procedures for ensuring the continued smooth operation of the Alfred Agent Platform. It covers monitoring, troubleshooting, scaling, backups, and handling incidents.

## 2. Monitoring & Alerting

### 2.1. Monitoring Tools

- **Prometheus**: Monitors system health, task processing times, error rates, and resource usage (CPU, memory)
- **Grafana**: Visualizes data collected from Prometheus, providing dashboards for performance metrics
- **Google Cloud Monitoring**: Monitors cloud infrastructure performance (e.g., Google Cloud Run services)

### 2.2. Alerts

Set up alerts for:
- Task failures (e.g., tasks that fail after retry attempts)
- System resource issues (e.g., high CPU/memory usage)
- Task processing time thresholds (e.g., tasks taking too long)
- Database connection limits (>80%)

### 2.3. Prometheus Configuration

```yaml
# Prometheus scrape config
scrape_configs:
  - job_name: 'agents'
    static_configs:
      - targets: ['alfred-bot:8011', 'social-intel:9000', 'legal-compliance:9002']
    metrics_path: '/metrics'
```

### 2.4. Example Grafana Dashboard Configuration

```json
{
  "panels": [
    {
      "title": "Task Processing Rate",
      "targets": [
        {
          "expr": "rate(tasks_processed_total[5m])"
        }
      ]
    },
    {
      "title": "Task Error Rate",
      "targets": [
        {
          "expr": "rate(tasks_errors_total[5m])"
        }
      ]
    }
  ]
}
```

### 2.5. Available Dashboards

- Platform Overview: http://localhost:3002/d/alfred-overview
- Financial-Tax Dashboard: http://localhost:3002/d/financial-tax
- System Metrics: http://localhost:9090/graph
- Agent Comparison Dashboard

## 3. Scaling

### 3.1. Horizontal Scaling

- **Microservices**: Use Kubernetes or Google Cloud Run for auto-scaling services (agents, API)
- **Pub/Sub**: Automatically scales with message volume, ensuring message delivery to agents without bottlenecks
- **Autoscale Configuration**: Cloud Run `maxInstances=20`, `minInstances=0`

### 3.2. Database Scaling

- **Supabase**: Scale Postgres database horizontally (using read replicas or partitioning) to handle high volumes of state storage
- **Qdrant**: Scale vector search using Qdrant clusters
- **Connection Pooling**: Configure appropriate connection pool sizes for optimal performance

### 3.3. Scaling Triggers

- Scale up when:
  - Task queue length exceeds 1,000 messages for 5 minutes
  - CPU utilization exceeds 80% for more than 2 minutes
  - Memory utilization exceeds 80% for more than 2 minutes
- Scale down when:
  - Resource utilization falls below 40% for 10 minutes

## 4. Backups & Data Recovery

### 4.1. Regular Backups

- Schedule automated backups for the Postgres database (Supabase) and Qdrant vector store
- Store backups off-site (e.g., cloud storage) to ensure data redundancy
- Backup frequency:
  - Daily full backups
  - Hourly incremental backups
  - Transaction log backups every 15 minutes

### 4.2. Backup Script Example

```bash
#!/bin/bash
# Postgres database backup
pg_dump $SUPABASE_URL > backup_$(date +%Y%m%d).sql
aws s3 cp backup_$(date +%Y%m%d).sql s3://backups/
```

### 4.3. Restore Script Example

```bash
#!/bin/bash
# Restore from backup
aws s3 cp s3://backups/backup_20240502.sql .
psql $SUPABASE_URL < backup_20240502.sql
```

### 4.4. Disaster Recovery

- Implement disaster recovery procedures to restore system operations in case of data loss or system failures
- Ensure a rollback mechanism for database migrations or failed deployments
- Test recovery procedures regularly to ensure they work as expected
- Document recovery time objectives (RTO) and recovery point objectives (RPO)

## 5. Routine Maintenance

### 5.1. Database Maintenance

- Run VACUUM ANALYZE on Postgres databases weekly
- Manage processed_msgs table to prevent excessive growth
- Monitor and optimize database indexes

```sql
-- Cleanup script for processed_msgs table
DELETE FROM processed_msgs WHERE processed_at < NOW() - INTERVAL '48 hours';
```

### 5.2. Docker Image Management

- Clean up unused Docker images monthly
- Tag stable images with version numbers and 'latest' tag
- Implement image retention policies

```bash
# Clean up unused Docker images
docker image prune -a --filter "until=168h"
```

### 5.3. Log Rotation and Management

- Configure log rotation for all services
- Archive logs older than 30 days
- Ensure logs are appropriately structured for analysis

## 6. Troubleshooting & Incident Management

### 6.1. Logs & Diagnostics

- **Google Cloud Logging**: Collect logs from all services (agents, API, Pub/Sub) for debugging
- **LangSmith**: Use LangSmith for debugging agent workflows and tracing task processing issues
- **Tracing**: Implement distributed tracing with OpenTelemetry for end-to-end visibility

### 6.2. Common Issues and Solutions

#### Task Processing Failures

**Symptoms**:
- Tasks stuck in "processing" state
- High error rates in monitoring dashboards

**Troubleshooting Steps**:
1. Check agent logs for errors
2. Verify Pub/Sub connectivity
3. Check Supabase connection status
4. Examine LangSmith traces for LLM-related issues

**Resolution**:
- Restart affected agent services
- Clear stuck tasks from processing queue
- Fix underlying issue (e.g., API key, rate limits)

#### Database Connection Issues

**Symptoms**:
- "Connection refused" errors in logs
- Slow query performance

**Troubleshooting Steps**:
1. Check database status and connection limits
2. Verify network connectivity
3. Check for locks or long-running queries

**Resolution**:
- Optimize connection pooling
- Terminate blocking queries if necessary
- Scale database resources if needed

### 6.3. Incident Response

Set up an incident response plan for handling system outages, task processing failures, or security breaches:

1. **Detection**: 
   - Monitor alerts and logs
   - Establish on-call rotation

2. **Triage**:
   - Assess impact and priority
   - Assign incident owner

3. **Resolution**:
   - Identify root cause
   - Implement fix or workaround
   - Communicate status to stakeholders

4. **Post-mortem**:
   - Document what happened
   - Identify preventative measures
   - Implement improvements

## 7. Upgrade Procedures

### 7.1. Service Upgrades

1. Create a detailed upgrade plan
2. Test upgrades in staging environment
3. Take backup before production upgrade
4. Perform rolling upgrades when possible
5. Verify functionality after upgrade
6. Have rollback plan ready

### 7.2. Database Schema Changes

1. Test migrations in development/staging
2. Back up production database before migration
3. Apply schema changes during maintenance window
4. Verify application compatibility with new schema
5. Monitor performance after migration

## 8. Security Maintenance

### 8.1. Regular Security Updates

- Apply security patches monthly or as needed
- Update dependencies to address vulnerabilities
- Conduct regular security audits

### 8.2. Secret Rotation

- Rotate API keys quarterly
- Update JWT signing keys annually
- Use secrets management solutions (e.g., Google Secret Manager)

## 9. Contact Information

For operations issues or questions:
- **Platform Team**: platform@alfred-ai.com
- **Incident Response**: incidents@alfred-ai.com