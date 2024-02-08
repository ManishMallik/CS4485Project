// Dashboard.js
import React from 'react';
import { Typography, Grid, Paper, Button, Link } from '@mui/material';

const Dashboard = () => {
  // Example Data
  const overviewData = {
    totalAttempts: 1000,
    regularAttempts: 800,
    attackAttempts: 20,
  };

  const recentAlerts = [
    { id: 1, type: 'Security Threat', description: 'Unusual activity detected', timestamp: '2022-02-01T12:30:00' },
    { id: 2, type: 'Login Failure', description: 'Multiple failed login attempts', timestamp: '2022-02-01T11:45:00' },
    { id: 3, type: 'Malware Detection', description: 'Malicious file detected', timestamp: '2022-02-01T10:15:00' },
  ];

  const performanceMetrics = {
    cpuUsage: 30,
    memoryUsage: 60,
    networkTraffic: 500,
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Security Dashboard
      </Typography>
      <Grid container spacing={3}>
        {/* Overview */}
        <Grid item xs={12} sm={6} md={4}>
          <Paper elevation={3} style={{ padding: '20px' }}>
            <Typography variant="h6" gutterBottom>
              Overview
            </Typography>
            <Typography variant="body1">Benign Attacks: {overviewData.totalAttempts}</Typography>
            <Typography variant="body1">DoS Attacks: {overviewData.regularAttempts}</Typography>
            <Typography variant="body1">Web Attacks: {overviewData.attackAttempts}</Typography>
            <br/>
            <Button variant="outlined" color="primary" onClick={() => console.log('Review and update user access permissions')}>
              Review User Permissions
            </Button>
          </Paper>
        </Grid>

        {/* Recent Alerts */}
        <Grid item xs={12} sm={6} md={4}>
          <Paper elevation={3} style={{ padding: '20px' }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            {recentAlerts.map((alert) => (
              <div key={alert.id}>
                <Typography variant="subtitle2">{alert.type}</Typography>
                <Typography variant="body2">{alert.description}</Typography>
                <Typography variant="caption">{new Date(alert.timestamp).toLocaleString()}</Typography>
                <hr />
              </div>
            ))}
            <br/>
            <Button variant="outlined" color="primary" onClick={() => console.log('Investigate recent security alerts')}>
              Investigate Alerts
            </Button>
          </Paper>
        </Grid>

        {/* Key Performance Metrics */}
        <Grid item xs={12} sm={12} md={4}>
          <Paper elevation={3} style={{ padding: '20px' }}>
            <Typography variant="h6" gutterBottom>
              Key Performance Metrics
            </Typography>
            <Typography variant="body1">CPU Usage: {performanceMetrics.cpuUsage}%</Typography>
            <Typography variant="body1">Memory Usage: {performanceMetrics.memoryUsage}%</Typography>
            <Typography variant="body1">Network Traffic: {performanceMetrics.networkTraffic} Mbps</Typography>
            <br/>
            <Button variant="outlined" color="primary" onClick={() => console.log('Optimize resource usage')}>
              Optimize Resources
            </Button>
          </Paper>
        </Grid>
      </Grid>

      {/* Additional Actionable Items */}
      <Typography variant="h5" style={{ marginTop: '20px' }} gutterBottom>
        Additional Actionable Items
      </Typography>
      <Link href="#" onClick={() => console.log('Initiate incident response procedures')}>
        Initiate Incident Response
      </Link>
      <br />
      <Link href="#" onClick={() => console.log('Review and update security policies')}>
        Review Security Policies
      </Link>
    </div>
  );
};

export default Dashboard;
