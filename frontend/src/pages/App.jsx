import React, { useEffect, useState } from 'react'
import { Container, Grid, Card, CardContent, Typography, FormControl, InputLabel, Select, MenuItem, Checkbox, ListItemText, OutlinedInput, Button } from '@mui/material'
import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000/api' })
const SUBTOPICS = ['AI', 'IoT', 'Cybersecurity', 'Data Science', 'Robotics', 'Medical Imaging', 'Genomics']

export default function App() {
  const [month, setMonth] = useState('2024-01')
  const [domain, setDomain] = useState('Information Technology')
  const [subtopics, setSubtopics] = useState(['AI'])
  const [overview, setOverview] = useState({ total: 0, domains: {}, subtopics: {}, sources: {} })
  const [top, setTop] = useState({ venues: {}, authors: {} })
  const [pubs, setPubs] = useState([])

  const fetchData = async () => {
    const [overviewResp, topResp, pubsResp] = await Promise.all([
      api.get(`/analytics/overview/${month}`),
      api.get(`/analytics/top/${month}`),
      api.get(`/analytics/publications/${month}`)
    ])
    setOverview(overviewResp.data)
    setTop(topResp.data)
    setPubs(pubsResp.data)
  }

  useEffect(() => { fetchData() }, [month])

  const filteredPubs = pubs.filter(p => p.domain === domain && (subtopics.length === 0 || p.subtopics.some(s => subtopics.includes(s))))
  const aiPercentage = overview.subtopics['AI'] ? Math.round((overview.subtopics['AI'] / (overview.total || 1)) * 100) : 0
  const iotPercentage = overview.subtopics['IoT'] ? Math.round((overview.subtopics['IoT'] / (overview.total || 1)) * 100) : 0

  return (
    <Container maxWidth="lg" sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>Paper Analytics Dashboard</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>Month</InputLabel>
            <Select value={month} label="Month" onChange={(e) => setMonth(e.target.value)}>
              {['2024-01', '2024-02', '2024-03', '2024-04'].map(m => <MenuItem key={m} value={m}>{m}</MenuItem>)}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={3}>
          <FormControl fullWidth>
            <InputLabel>Domain</InputLabel>
            <Select value={domain} label="Domain" onChange={(e) => setDomain(e.target.value)}>
              {['Information Technology', 'Medicine', 'Biology', 'Physics', 'Mathematics', 'Other'].map(d => <MenuItem key={d} value={d}>{d}</MenuItem>)}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Subtopics</InputLabel>
            <Select
              multiple
              value={subtopics}
              onChange={(e) => setSubtopics(e.target.value)}
              input={<OutlinedInput label="Subtopics" />}
              renderValue={(selected) => selected.join(', ')}
            >
              {SUBTOPICS.map(name => (
                <MenuItem key={name} value={name}>
                  <Checkbox checked={subtopics.indexOf(name) > -1} />
                  <ListItemText primary={name} />
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Grid container spacing={2} sx={{ marginTop: 2 }}>
        <Grid item xs={12} md={4}>
          <Card><CardContent>
            <Typography variant="h6">Total Papers</Typography>
            <Typography variant="h4">{overview.total}</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card><CardContent>
            <Typography variant="h6">AI %</Typography>
            <Typography variant="h4">{aiPercentage}%</Typography>
          </CardContent></Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card><CardContent>
            <Typography variant="h6">IoT %</Typography>
            <Typography variant="h4">{iotPercentage}%</Typography>
          </CardContent></Card>
        </Grid>
      </Grid>

      <Grid container spacing={2} sx={{ marginTop: 2 }}>
        <Grid item xs={12} md={6}>
          <Card><CardContent>
            <Typography variant="h6">Top Venues</Typography>
            {Object.entries(top.venues).map(([venue, count]) => (
              <Typography key={venue}>{venue}: {count}</Typography>
            ))}
          </CardContent></Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card><CardContent>
            <Typography variant="h6">Top Authors</Typography>
            {Object.entries(top.authors).map(([author, count]) => (
              <Typography key={author}>{author}: {count}</Typography>
            ))}
          </CardContent></Card>
        </Grid>
      </Grid>

      <Card sx={{ marginTop: 2 }}>
        <CardContent>
          <Typography variant="h6">Publications</Typography>
          {filteredPubs.map(pub => (
            <div key={pub.id} style={{ marginBottom: 8 }}>
              <Typography variant="subtitle1">{pub.title}</Typography>
              <Typography variant="body2">{pub.authors.map(a => a.name).join(', ')}</Typography>
              <Typography variant="caption">{pub.published_at} • {pub.source} • {pub.subtopics.join(', ')}</Typography>
            </div>
          ))}
        </CardContent>
      </Card>
    </Container>
  )
}
