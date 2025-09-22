import { useEffect, useState } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export default function ConverterPage() {
  const [file, setFile] = useState<File | null>(null)
  const [videoId, setVideoId] = useState<string | null>(null)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState<string | null>(null)

  async function upload() {
    if (!file) return
    setBusy(true)
    setMessage('Uploading...')
    try {
      const form = new FormData()
      form.append('file', file)
      const res = await fetch(`${API_BASE}/api/videos/upload`, { method: 'POST', body: form })
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
      const data = await res.json()
      setVideoId(data.video_id)
      setMessage('Uploaded')
    } catch (e: any) {
      setMessage(e.message || 'Upload failed')
    } finally {
      setBusy(false)
    }
  }

  async function convert() {
    if (!videoId) return
    setBusy(true)
    setMessage('Converting to WAV (16kHz mono)...')
    try {
      const res = await fetch(`${API_BASE}/api/videos/${videoId}/convert/audio`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ format: 'wav', sample_rate: 16000, channels: 1 })
      })
      if (!res.ok) throw new Error(`Conversion failed: ${res.status}`)
      const data = await res.json()
      const url = `${API_BASE}${data.url}`
      setAudioUrl(url)
      setMessage('Conversion complete')
    } catch (e: any) {
      setMessage(e.message || 'Conversion failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <main style={{ padding: 24, maxWidth: 720, margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>Converter</h1>
      <p>Upload a video and convert its audio track to WAV (16kHz mono).</p>

      <section style={{ marginTop: 24 }}>
        <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button onClick={upload} disabled={!file || busy} style={{ marginLeft: 8 }}>Upload</button>
        {videoId && <p>Video ID: <code>{videoId}</code></p>}
      </section>

      <section style={{ marginTop: 24 }}>
        <button onClick={convert} disabled={!videoId || busy}>Convert to WAV</button>
      </section>

      {message && <p style={{ marginTop: 16 }}>{message}</p>}

      {audioUrl && (
        <section style={{ marginTop: 24 }}>
          <h3>Result</h3>
          <audio controls src={audioUrl} style={{ width: '100%' }} />
          <p><a href={audioUrl} download>Download WAV</a></p>
        </section>
      )}
    </main>
  )
}
