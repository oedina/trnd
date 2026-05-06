<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SeasonalRank — Sign In</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=DM+Sans:wght@300;400;500&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
<style>
:root{--cream:#F7F3EE;--ink:#1C1917;--rose:#C4826A;--gold:#B89A6A;--fog:#E2DDD7;--warm:#FBF8F5;--sage:#8A9E8C}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--cream);color:var(--ink);font-family:'DM Sans',sans-serif;font-weight:300;min-height:100vh;display:flex;flex-direction:column}

.page{flex:1;display:grid;grid-template-columns:1fr 1fr;min-height:100vh}

/* LEFT — editorial panel */
.left-panel{background:var(--ink);display:flex;flex-direction:column;justify-content:space-between;padding:2.5rem;position:relative;overflow:hidden}
.left-panel::before{content:'';position:absolute;top:-60px;right:-60px;width:300px;height:300px;border-radius:50%;background:var(--rose);opacity:.08}
.left-panel::after{content:'';position:absolute;bottom:-80px;left:-40px;width:240px;height:240px;border-radius:50%;background:var(--gold);opacity:.06}
.left-logo{font-family:'Playfair Display',serif;font-size:28px;font-weight:900;color:var(--cream);letter-spacing:-.04em}
.left-logo span{font-style:italic;color:var(--rose)}
.left-mid{position:relative;z-index:1}
.left-headline{font-family:'DM Serif Display',serif;font-size:clamp(28px,4vw,44px);font-style:italic;color:var(--cream);line-height:1.1;margin-bottom:1rem}
.left-headline em{font-style:normal;color:var(--rose)}
.left-sub{font-size:12px;color:rgba(255,255,255,.45);line-height:1.7;max-width:280px}
.left-stats{display:flex;gap:1.5rem}
.left-stat-num{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:var(--cream);line-height:1}
.left-stat-label{font-size:7px;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.35);margin-top:3px}

/* RIGHT — form panel */
.right-panel{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:3rem 2rem;background:var(--warm)}
.form-wrap{width:100%;max-width:360px}
.form-title{font-family:'DM Serif Display',serif;font-size:26px;font-style:italic;margin-bottom:.3rem}
.form-sub{font-size:11px;color:var(--gold);letter-spacing:.08em;margin-bottom:2rem}

/* SOCIAL BUTTONS */
.social-btn{width:100%;display:flex;align-items:center;gap:.85rem;padding:.75rem 1rem;border:1px solid var(--fog);background:white;cursor:pointer;font-family:'DM Sans',sans-serif;font-size:12px;font-weight:400;color:var(--ink);transition:all .18s;margin-bottom:.6rem;text-decoration:none}
.social-btn:hover{background:var(--cream);border-color:var(--ink)}
.social-btn svg{flex-shrink:0}
.social-btn-text{flex:1;text-align:center}

.divider{display:flex;align-items:center;gap:.75rem;margin:1.25rem 0}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:var(--fog)}
.divider span{font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}

/* FORM FIELDS */
.field{margin-bottom:.85rem}
.field label{display:block;font-size:8px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:.35rem}
.field input{width:100%;padding:.65rem .9rem;border:1px solid var(--fog);background:white;font-family:'DM Sans',sans-serif;font-size:12px;color:var(--ink);outline:none;transition:border-color .2s}
.field input:focus{border-color:var(--ink)}
.field input::placeholder{color:#c8c4bc}

.forgot{display:block;text-align:right;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);text-decoration:none;margin-top:-0.5rem;margin-bottom:1rem}
.forgot:hover{color:var(--rose)}

.submit-btn{width:100%;padding:.75rem;background:var(--ink);color:var(--cream);border:none;cursor:pointer;font-family:'DM Sans',sans-serif;font-size:10px;letter-spacing:.22em;text-transform:uppercase;transition:background .2s;margin-bottom:1.25rem}
.submit-btn:hover{background:var(--rose)}

.form-footer{text-align:center;font-size:10px;color:var(--gold)}
.form-footer a{color:var(--rose);text-decoration:none}
.form-footer a:hover{text-decoration:underline}

/* TABS */
.tabs{display:flex;gap:0;margin-bottom:1.5rem;border-bottom:1px solid var(--fog)}
.tab-btn{flex:1;padding:.6rem;background:none;border:none;border-bottom:2px solid transparent;font-family:'DM Sans',sans-serif;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);cursor:pointer;transition:all .15s;margin-bottom:-1px}
.tab-btn.active{color:var(--ink);border-bottom-color:var(--ink)}

/* ERROR / SUCCESS */
.msg{font-size:10px;padding:.5rem .75rem;margin-bottom:.75rem;display:none}
.msg.error{background:#fde8e8;color:#7a1f1f;border-left:2px solid #e05c5c}
.msg.success{background:#eaf3de;color:#27500a;border-left:2px solid #7ecf8a}
.msg.show{display:block}

@media(max-width:640px){
  .page{grid-template-columns:1fr}
  .left-panel{display:none}
  .right-panel{padding:2rem 1.25rem;background:var(--cream)}
}
</style>
</head>
<body>
<div class="page">

  <!-- LEFT PANEL -->
  <div class="left-panel">
    <div class="left-logo">Seasonal<span>Rank</span></div>
    <div class="left-mid">
      <div class="left-headline">Track what <em>America</em><br>is wearing — weekly</div>
      <div class="left-sub">Join thousands of fashion enthusiasts and small brands using real trend data to stay ahead of the curve.</div>
    </div>
    <div class="left-stats">
      <div>
        <div class="left-stat-num">20</div>
        <div class="left-stat-label">Styles tracked</div>
      </div>
      <div>
        <div class="left-stat-num">4</div>
        <div class="left-stat-label">Data sources</div>
      </div>
      <div>
        <div class="left-stat-num">Weekly</div>
        <div class="left-stat-label">Updates</div>
      </div>
    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div class="right-panel">
    <div class="form-wrap">
      <div class="form-title">Welcome back</div>
      <div class="form-sub">Sign in to save your votes and preferences</div>

      <!-- TABS -->
      <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('signin')">Sign in</button>
        <button class="tab-btn" onclick="switchTab('signup')">Create account</button>
      </div>

      <!-- ERROR/SUCCESS MSG -->
      <div class="msg" id="formMsg"></div>

      <!-- SOCIAL LOGIN -->
      <a class="social-btn" href="#" onclick="socialLogin('Google')">
        <svg width="18" height="18" viewBox="0 0 18 18"><path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.875 2.684-6.615z" fill="#4285F4"/><path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 009 18z" fill="#34A853"/><path d="M3.964 10.71A5.41 5.41 0 013.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 000 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05"/><path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 00.957 4.958L3.964 6.29C4.672 4.163 6.656 3.58 9 3.58z" fill="#EA4335"/></svg>
        <span class="social-btn-text">Continue with Google</span>
      </a>
      <a class="social-btn" href="#" onclick="socialLogin('Apple')">
        <svg width="18" height="18" viewBox="0 0 814 1000"><path d="M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76 0-103.7 40.8-165.9 40.8s-105-37.5-155.5-127.4C46 423.1 0 248.1 0 181.6c0-136.4 89.5-208.8 175.9-208.8 79.8 0 130.4 52.1 181.7 52.1 48.3 0 106.7-55.2 190.5-55.2zm-114.9-126.4c38.4-45.5 65.3-109.5 65.3-173.5 0-8.9-.7-17.9-2.3-25.8-62.1 2.3-136.8 41.2-181.7 93.7-34.7 39.5-67.9 103.6-67.9 168.3 0 9.6 1.6 19.3 2.3 22.6 3.9.7 10.3 1.6 16.6 1.6 55.2 0 126.2-37.5 167.7-86.9z" fill="var(--ink)"/></svg>
        <span class="social-btn-text">Continue with Apple</span>
      </a>

      <div class="divider"><span>or</span></div>

      <!-- SIGN IN FORM -->
      <div id="signinForm">
        <div class="field">
          <label>Email address</label>
          <input type="email" id="siEmail" placeholder="you@example.com">
        </div>
        <div class="field">
          <label>Password</label>
          <input type="password" id="siPass" placeholder="••••••••">
        </div>
        <a href="#" class="forgot">Forgot password?</a>
        <button class="submit-btn" onclick="doSignIn()">Sign in</button>
        <div class="form-footer">Don't have an account? <a href="#" onclick="switchTab('signup')">Create one free</a></div>
      </div>

      <!-- SIGN UP FORM -->
      <div id="signupForm" style="display:none">
        <div class="field">
          <label>Full name</label>
          <input type="text" id="suName" placeholder="Your name">
        </div>
        <div class="field">
          <label>Email address</label>
          <input type="email" id="suEmail" placeholder="you@example.com">
        </div>
        <div class="field">
          <label>Password</label>
          <input type="password" id="suPass" placeholder="Min. 8 characters">
        </div>
        <button class="submit-btn" onclick="doSignUp()">Create account</button>
        <div class="form-footer">Already have an account? <a href="#" onclick="switchTab('signin')">Sign in</a></div>
      </div>

    </div>
  </div>
</div>

<script>
function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach((b,i) => b.classList.toggle('active', (i===0&&tab==='signin')||(i===1&&tab==='signup')));
  document.getElementById('signinForm').style.display = tab==='signin'?'block':'none';
  document.getElementById('signupForm').style.display = tab==='signup'?'block':'none';
  hideMsg();
}

function showMsg(text, type) {
  const el = document.getElementById('formMsg');
  el.textContent = text;
  el.className = 'msg ' + type + ' show';
}
function hideMsg() {
  document.getElementById('formMsg').className = 'msg';
}

function doSignIn() {
  const email = document.getElementById('siEmail').value.trim();
  const pass  = document.getElementById('siPass').value;
  if (!email || !pass) { showMsg('Please fill in all fields.', 'error'); return; }
  if (!email.includes('@')) { showMsg('Please enter a valid email.', 'error'); return; }
  // Check localStorage for registered users
  const users = JSON.parse(localStorage.getItem('sr_users') || '{}');
  if (!users[email]) { showMsg('No account found. Please create one.', 'error'); return; }
  if (users[email].password !== btoa(pass)) { showMsg('Incorrect password. Please try again.', 'error'); return; }
  // Success — store session
  localStorage.setItem('sr_session', JSON.stringify({email, name: users[email].name, role: users[email].role || 'user'}));
  showMsg('Signing in...', 'success');
  setTimeout(() => {
    const next = new URLSearchParams(window.location.search).get('next') || 'index.html';
    window.location.href = next;
  }, 800);
}

function doSignUp() {
  const name  = document.getElementById('suName').value.trim();
  const email = document.getElementById('suEmail').value.trim();
  const pass  = document.getElementById('suPass').value;
  if (!name || !email || !pass) { showMsg('Please fill in all fields.', 'error'); return; }
  if (!email.includes('@')) { showMsg('Please enter a valid email.', 'error'); return; }
  if (pass.length < 8) { showMsg('Password must be at least 8 characters.', 'error'); return; }
  const users = JSON.parse(localStorage.getItem('sr_users') || '{}');
  if (users[email]) { showMsg('An account already exists with this email.', 'error'); return; }
  // Register — first user becomes admin
  const isFirst = Object.keys(users).length === 0;
  users[email] = {name, password: btoa(pass), role: isFirst ? 'admin' : 'user', joined: new Date().toISOString()};
  localStorage.setItem('sr_users', JSON.stringify(users));
  localStorage.setItem('sr_session', JSON.stringify({email, name, role: users[email].role}));
  showMsg('Account created! Redirecting...', 'success');
  setTimeout(() => { window.location.href = 'index.html'; }, 900);
}

function socialLogin(provider) {
  // Simulate OAuth — in production replace with real OAuth flow
  const name  = prompt(`Enter your name to continue with ${provider}:`);
  if (!name) return;
  const email = prompt('Enter your email:');
  if (!email || !email.includes('@')) { showMsg('Invalid email.', 'error'); return; }
  const users = JSON.parse(localStorage.getItem('sr_users') || '{}');
  if (!users[email]) {
    const isFirst = Object.keys(users).length === 0;
    users[email] = {name, password: '', role: isFirst ? 'admin' : 'user', provider, joined: new Date().toISOString()};
    localStorage.setItem('sr_users', JSON.stringify(users));
  }
  localStorage.setItem('sr_session', JSON.stringify({email, name: users[email].name, role: users[email].role}));
  window.location.href = 'index.html';
}

// If already logged in, redirect
const session = JSON.parse(localStorage.getItem('sr_session') || 'null');
if (session) window.location.href = 'index.html';
</script>
</body>
</html>
