const sound = document.getElementById('popsound');
const nyanCat = document.getElementById('nyan-cat');
const meow = document.getElementById('meosound');

nyanCat.addEventListener('click', () => {
  meow.play();
});

nyanCat.addEventListener('touchstart', () => {
  meow.play();
});

const messages = [
  "Anh yêu em 💕", "Anh thương em 🤗", "I Love You 🥰", "Em thật xinh đẹp",
  "Hạnh phúc nhé 💫", "❤️ Gửi yêu thương ❤️", "Luôn mỉm cười nhé 😊",
  "Love You 3000 💖", "Cảm ơn vì tất cả 🌸",
  "Em là một món quà 🎁", "Trái tim này là của em 💘",
  "Em làm thế giới này đẹp hơn 💐", "Love You In Every Universe",
  "Em là duy nhất 💞", "Saranghaeyo❤️",
  "Anh nhớ em nhiều 🌈", "You Are My Everything 🫶",
  "Yêu em không cần lý do 🏡", "Em là lý do anh luôn mỉm cười 😘",
  "Anh yêu em vì em là chính em ✨"
];

function showRandomMessage(event) {
  sound.play();
  const msg = document.createElement("div");
  msg.className = "message";
  msg.textContent = messages[Math.floor(Math.random() * messages.length)];

  const directions = [0, Math.PI/4, Math.PI/2, 3*Math.PI/4, Math.PI, 5*Math.PI/4, 3*Math.PI/2, 7*Math.PI/4];
  const angle = directions[Math.floor(Math.random() * directions.length)];
  const distance = 200;
  const dx = Math.cos(angle) * distance + "px";
  const dy = Math.sin(angle) * distance + "px";
  msg.style.setProperty('--dx', dx);
  msg.style.setProperty('--dy', dy);

  const rect = event.currentTarget.getBoundingClientRect();
  msg.style.left = rect.left + rect.width / 2 + "px";
  msg.style.top = rect.top + rect.height / 2 + "px";
  msg.style.transform = "translate(-50%, -50%)";
  msg.style.position = "fixed";

  document.body.appendChild(msg);

  setTimeout(() => msg.remove(), 3000);
}
