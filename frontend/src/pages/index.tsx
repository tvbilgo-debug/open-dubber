import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null)
  const [videoId, setVideoId] = useState<string | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)
  const [status, setStatus] = useState<any>(null)
  const [lang, setLang] = useState<string>('es')

  async function upload() {
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    const res = await fetch(`${API_BASE}/api/videos/upload`, {
      method: 'POST',
      body: form,
    })
    if (!res.ok) {
      alert('Upload failed')
      return
    }
    const data = await res.json()
    setVideoId(data.video_id)
  }

  async function startJob() {
    if (!videoId) return
    const res = await fetch(`${API_BASE}/api/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ video_id: videoId, target_languages: [lang] }),
    })
    if (!res.ok) {
      alert('Job creation failed')
      return
    }
    const data = await res.json()
    setJobId(data.job_id)
  }

  useEffect(() => {
    if (!jobId) return
    const t = setInterval(async () => {
      const res = await fetch(`${API_BASE}/api/jobs/${jobId}`)
      const data = await res.json()
      setStatus(data)
      if (data.state === 'SUCCESS' || data.state === 'FAILURE') {
        clearInterval(t)
      }
    }, 1500)
    return () => clearInterval(t)
  }, [jobId])

  return (
    <main style={{ padding: 24, maxWidth: 720, margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>Open Dubber</h1>
      <p>Upload a video, then run a dummy translation/dubbing job.</p>

      <p><Link href="/converter">Go to Converter</Link></p>

      <section style={{ marginTop: 24 }}>
        <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button onClick={upload} disabled={!file} style={{ marginLeft: 8 }}>Upload</button>
        {videoId && <p>Video ID: <code>{videoId}</code></p>}
      </section>

      <section style={{ marginTop: 24 }}>
        <label>
          Target language:
          <input value={lang} onChange={(e) => setLang(e.target.value)} style={{ marginLeft: 8 }} />
        </label>
        <button onClick={startJob} disabled={!videoId} style={{ marginLeft: 8 }}>Start Job</button>
        {jobId && <p>Job ID: <code>{jobId}</code></p>}
      </section>

      <section style={{ marginTop: 24 }}>
        <h3>Status</h3>
        <pre style={{ background: '#f6f6f6', padding: 12 }}>{status ? JSON.stringify(status, null, 2) : 'No status yet'}</pre>
      </section>
    </main>
  )
}
