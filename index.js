const { Client, GatewayIntentBits } = require('discord.js');
const { token } = require('./config.json');

// 새로운 클라이언트를 생성합니다.
const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

// 봇이 준비되었을 때 실행될 코드를 작성합니다.
client.once('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

// 메시지를 수신하고 처리하는 코드입니다.
client.on('messageCreate', message => {
  // 봇이 보낸 메시지는 무시합니다.
  if (message.author.bot) return;

  // 사용자가 "!hello"라고 입력하면 환영 메시지를 보냅니다.
  if (message.content === '!hello') {
    message.channel.send(`안녕하세요, ${message.author}! 체리 봇입니다. 무엇을 도와드릴까요?`);
  }
});

// 봇을 로그인합니다.
client.login(token);
