css = '''
<style>
.chat-message{
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; dislay: flex
}
.chat-message.user{
    bacground-color: gray;
}
.chat-message.bot{
    backgroung-color: blue;
}
.chat-message.avatar{
    width: 15%;
}
.chat-message.avatar img{
    max-width: 78px;
    max-height: 78px;
    boder-radius: 50%;
    object-fit: cover;
}
.chat-message .message{
    width: 85%
    padding: 0 1.5rem;
    color: white;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
    <img>
    </div>
    <div class="message">SMSG</div>
    </div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
    <img>
    </div>
    <div class="message">SMSG</div>
    </div>
'''