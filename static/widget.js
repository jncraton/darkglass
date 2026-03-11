;(() => {
  const styles = `
    #darkglass {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 300px;
      max-width: 80vw;
      font-family: sans-serif;
      font-size: 14px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      border: 1px solid #ccc;
      border-radius: 8px;
      overflow: hidden;
      z-index: 9999;
      transition: height 0.3s ease
    }
    #darkglass.closed {
      height: 40px;
      width: 200px
    }
    #darkglass .header {
      background: #007bff;
      color: #fff;
      padding: 8px 10px;
      cursor: pointer;
      user-select: none
    }
    #darkglass .body {
      display: flex;
      flex-direction: column;
      height: 300px;
      background: #fff
    }
    #darkglass.closed .body {
      display: none
    }
    #darkglass .messages {
      flex: 1;
      padding: 10px;
      overflow: auto;
      background: #fafafa
    }
    #darkglass .input-container {
      border-top: 1px solid #ddd;
      padding: 5px
    }
    #darkglass .input-container input {
      width: 100%;
      box-sizing: border-box;
      padding: 6px;
      border: 1px solid #ccc;
      border-radius: 4px
    }
  `

  const style = document.createElement('style')
  style.textContent = styles
  document.head.appendChild(style)

  const container = document.createElement('div')
  container.id = 'darkglass'
  container.className = 'closed'

  container.innerHTML = `
    <div class="header">Chat</div>
    <div class="body">
      <div class="messages"></div>
      <div class="input-container">
        <input type="text" placeholder="Ask a question...">
      </div>
    </div>
  `

  const header = container.querySelector('.header')
  const body = container.querySelector('.messages')
  const input = container.querySelector('input')

  header.addEventListener('click', (e) => {
    e.stopPropagation()
    container.classList.toggle('closed')
    if (!container.classList.contains('closed')) {
      input.focus()
    }
  })

  // prevent clicks inside the input from bubbling; we only want an outside
  // click to collapse the widget
  input.addEventListener('click', (e) => {
    e.stopPropagation()
  })

  // clicking anywhere else should collapse if open
  document.addEventListener('click', (e) => {
    if (!container.classList.contains('closed')) {
      if (!container.contains(e.target)) {
        container.classList.add('closed')
      }
    }
  })
  input.addEventListener('keydown', async (e) => {
    if (e.key === 'Enter') {
      const text = input.value.trim()
      if (!text) return

      const p = document.createElement('div')
      p.textContent = 'You: ' + text
      body.appendChild(p)

      input.value = ''

      try {
        const r = await fetch('/chat', {
          method: 'POST',
          headers: {'content-type': 'application/json'},
          body: JSON.stringify({message: text}),
        })
        const j = await r.json()
        const q = document.createElement('div')
        q.textContent = 'Agent: ' + j.answer
        body.appendChild(q)
        body.scrollTop = body.scrollHeight
      } catch (err) {
        console.error(err)
      }
    }
  })

  document.body.appendChild(container)
})()
