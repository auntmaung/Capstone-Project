import React, { useState } from 'react'

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const handleLogin = async () => {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    const data = await res.json()
    setMessage(data.message || data.detail)
  }

  const handleRegister = async () => {
    const res = await fetch("/api/register", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    const data = await res.json()
    setMessage(data.message || data.detail)
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Login App</h1>
      <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} /><br />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} /><br />
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleRegister}>Register</button>
      <p>{message}</p>
    </div>
  )
}

export default App
