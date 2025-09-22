import { useEffect, useState } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export default function ConverterPage() {
  const [file, setFile] = useState<File | null>(null)
  const [videoId, setVideoId] = useState<string | null>(null)
  const [jobId, setJobId] = useState<string | null>(null)
  const [status, setStatus] = useState<any>(null)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState<string | null>(null)

  const [fmt, setFmt] = useState<'wav' | 'mp3'>('wav')
  const [bitrate, setBitrate] = useState<string>('128k')
  const [sampleRate, setSampleRate] = useState<number>(16000)
  const [channels, setChannels] = useState<number>(1)

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
    setMessage(`Starting ${fmt.toUpperCase()} conversion...`)
    setAudioUrl(null)
    setStatus(null)
    try {
      const res = await fetch(`${API_BASE}/api/videos/${videoId}/convert/audio`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ format: fmt, sample_rate: sampleRate, channels, bitrate: fmt === 'mp3' ? bitrate : undefined })
      })
      if (!res.ok) throw new Error(`Conversion creation failed: ${res.status}`)
      const data = await res.json()
      setJobId(data.job_id)
      setMessage('Job queued...')
    } catch (e: any) {
      setMessage(e.message || 'Conversion failed to start')
      setBusy(false)
    }
  }

  useEffect(() => {
    if (!jobId) return
    const t = setInterval(async () => {
      const res = await fetch(`${API_BASE}/api/jobs/${jobId}`)
      const data = await res.json()
      setStatus(data)
      if (data.state === 'SUCCESS') {
        const url = `${API_BASE}${data.meta.url}`
        setAudioUrl(url)
        setMessage('Conversion complete')
        setBusy(false)
        clearInterval(t)
      } else if (data.state === 'FAILURE') {
        setMessage(data.meta?.detail || 'Conversion failed')
        setBusy(false)
        clearInterval(t)
      }
    }, 1500)
    return () => clearInterval(t)
  }, [jobId])

  return (
    <main style={{ padding: 24, maxWidth: 720, margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h1>Converter</h1>
      <p>Upload a video and convert its audio track to WAV or MP3.</p>

      <section style={{ marginTop: 24 }}>
        <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button onClick={upload} disabled={!file || busy} style={{ marginLeft: 8 }}>Upload</button>
        {videoId && <p>Video ID: <code>{videoId}</code></p>}
      </section>

      <section style={{ marginTop: 24, display: 'flex', gap: 12, alignItems: 'center' }}>
        <label>
          Format:
          <select value={fmt} onChange={(e) => setFmt(e.target.value as 'wav' | 'mp3')} style={{ marginLeft: 8 }}>
            <option value="wav">WAV</option>
            <option value="mp3">MP3</option>
          </select>
        </label>
        {fmt === 'mp3' && (
          <label>
            Bitrate:
            <input value={bitrate} onChange={(e) => setBitrate(e.target.value)} style={{ marginLeft: 8, width: 100 }} placeholder="128k" />
          </label>
        )}
        <label>
          Sample rate:
          <input type="number" value={sampleRate} onChange={(e) => setSampleRate(parseInt(e.target.value || '16000', 10))} style={{ marginLeft: 8, width: 100 }} />
        </label>
        <label>
          Channels:
          <input type="number" value={channels} onChange={(e) => setChannels(parseInt(e.target.value || '1', 10))} style={{ marginLeft: 8, width: 60 }} />
        </label>
        <button onClick={convert} disabled={!videoId || busy}>Start Conversion</button>
      </section>

      {message && <p style={{ marginTop: 16 }}>{message}</p>}

      {status && (
        <pre style={{ background: '#f6f6f6', padding: 12 }}>{JSON.stringify(status, null, 2)}</pre>
      )}

      {audioUrl && (
        <section style={{ marginTop: 24 }}>
          <h3>Result</h3>
          <audio controls src={audioUrl} style={{ width: '100%' }} />
          <p><a href={audioUrl} download>Download {fmt.toUpperCase()}</a></p>
        </section>
      )}
    </main>
  )
}
