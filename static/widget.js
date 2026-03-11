;(function () {
  /*
  A self-contained chat widget.  Styles are kept minimal and inline
  so there are no external dependencies.  The box lives fixed in the
  bottom right corner and starts collapsed to a header bar.  Clicking
  the header inverts the ``closed`` state, showing the message area and
  input field.  The transition and flexible sizing make the widget
  behave responsively without any framework.
  */

  var style = document.createElement('style')
  style.textContent = {
    '#darkglass': {
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '300px',
      maxWidth: '80vw',
      maxHeight: '60vh',
      fontFamily: 'sans-serif',
      fontSize: '14px',
      boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
      border: '1px solid #ccc',
      borderRadius: '8px',
      overflow: 'hidden',
      zIndex: '9999',
      transition: 'max-height 0.3s ease,width 0.3s ease',
      /* height will be limited by max-height; closed/open controlled by class */
    },
    '#darkglass.closed': {
      maxHeight: '40px',
      width: '200px',
    },
    '#darkglass:not(.closed)': {
      maxHeight: '60vh',
    },
    '#darkglass .header': {
      background: '#007bff',
      color: '#fff',
      padding: '8px 10px',
      cursor: 'pointer',
      userSelect: 'none',
    },
    '#darkglass .body': {
      display: 'flex',
      flexDirection: 'column',
      height: '300px',
    },
    '#darkglass .messages': {
      flex: '1',
      padding: '10px',
      overflow: 'auto',
      background: '#fafafa',
    },
    '#darkglass .input-container': {
      borderTop: '1px solid #ddd',
      padding: '5px',
    },
    '#darkglass .input-container input': {
      width: '100%',
      boxSizing: 'border-box',
      padding: '6px',
      border: '1px solid #ccc',
      borderRadius: '4px',
    },
  }
  // convert style object to string
  style.textContent = Object.entries(style.textContent)
    .map(function (pair) {
      var selector = pair[0]
      var rules = pair[1]
      var body = Object.entries(rules)
        .map(function (r) {
          return r[0] + ':' + r[1] + ';'
        })
        .join('')
      return selector + '{' + body + '}'
    })
    .join('')
  document.head.appendChild(style)

  var container = document.createElement('div')
  container.id = 'darkglass'
  container.classList.add('closed')

  var header = document.createElement('div')
  header.className = 'header'
  header.textContent = 'Chat with us'
  container.appendChild(header)

  var body = document.createElement('div')
  body.className = 'body'

  var messages = document.createElement('div')
  messages.className = 'messages'
  body.appendChild(messages)

  var inputContainer = document.createElement('div')
  inputContainer.className = 'input-container'
  var input = document.createElement('input')
  input.type = 'text'
  input.placeholder = 'Ask a question...'
  inputContainer.appendChild(input)
  body.appendChild(inputContainer)

  container.appendChild(body)

  header.addEventListener('click', function () {
    container.classList.toggle('closed')
    if (!container.classList.contains('closed')) {
      input.focus()
    }
  })

  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var text = input.value.trim()
      if (!text) return
      var p = document.createElement('div')
      p.textContent = 'You: ' + text
      messages.appendChild(p)
      fetch('/chat', {
        method: 'POST',
        headers: {'content-type': 'application/json'},
        body: JSON.stringify({message: text}),
      })
        .then(function (r) {
          return r.json()
        })
        .then(function (j) {
          var q = document.createElement('div')
          q.textContent = 'Agent: ' + j.answer
          messages.appendChild(q)
          messages.scrollTop = messages.scrollHeight
        })
      input.value = ''
    }
  })

  document.body.appendChild(container)
})()
