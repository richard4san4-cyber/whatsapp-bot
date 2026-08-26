const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys')
const pino = require('pino')
const express = require('express')
const app = express()
const PORT = process.env.PORT || 10000

app.get('/', (req,res) => res.send('WhatsApp Bot is running'))
app.listen(PORT, () => console.log(`Bot running on ${PORT}`))

console.log('Starting bot...')

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState('./auth_info_baileys')
    
    const sock = makeWASocket({
        auth: state,
        logger: pino({ level: 'silent' }),
        printQRInTerminal: false,
        browser: ['WhatsApp Bot', 'Chrome', '1.0.0']
    })

    sock.ev.on('creds.update', saveCreds)

    if(!sock.authState.creds.registered){
      const phoneNumber = '2348033719309'
      setTimeout(async () => {
        try {
          const code = await sock.requestPairingCode(phoneNumber)
          console.log('====================================')
          console.log('PAIRING CODE:', code)
          console.log('Go to WhatsApp > Linked Devices > Link with phone number')
          console.log('====================================')
        } catch(e) {
          console.log('Error getting code:', e)
        }
      }, 8000)
    }

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect } = update
        if(connection === 'close') {
            const shouldReconnect = (lastDisconnect.error)?.output?.statusCode !== DisconnectReason.loggedOut
            console.log('Connection closed. Reconnecting:', shouldReconnect)
            if(shouldReconnect) setTimeout(startBot, 5000)
        } else if(connection === 'open') {
            console.log('Connected to WhatsApp!')
        }
    })

    sock.ev.on('messages.upsert', async m => {
        const msg = m.messages[0]
        if(!msg.message || msg.key.fromMe) return
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text || ''
        console.log('Message from:', msg.key.remoteJid, 'Body:', text)
        await sock.sendMessage(msg.key.remoteJid, { text: `You said: ${text}` })
    })
}

startBot()
