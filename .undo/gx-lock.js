/* gx-lock.js - change 156: password screen, and unscrambles the league data (espn-data.enc.js) for the app and the AI pages */
(function () {
  if (window.gxLoadData156) return;
  var W = { salt: "B5CJQJEcG4zzWrMfWN1XmQ==", iv: "YxLGc5MTv8hSWBLo", wk: "CttstgMvGahJLi7D+F2W0GMEAkclEWyYHY6lqagJKyoz0DCSNYSKivFcJmXFnaKyMMaEyeWbAnUk0QdvyUD1EHWK9bGiLTu2ANEBdDfjCexE2K3WHJpWQkDEWpj59/lw6OAoHQPYoLzju72NFHsBZnsuWWADp9eC8KM/92QAZl9cfMOX2/nL3auzYAloAT9QLgQmunpSwgaJz0FJ/XnKP+rCdRUSgOPcoAFsXPuQgj8bQRb/c3ygsBNgvhp/Syot36eT9IufqtRkMmzfEa3xFFQMf3GTnQEOegg1/20TXNoQayfkhfJLRLIzWWLYT/eCei1w9XrnuBn10rOt85dBd4oovjPK6fURLGZc2ZT3m01wBFZDTY/PLoryzUO5Kt8s+tV2Y8+956Ug1yQFejLNyqO0gJHJPS/3Oqy/Cl6aFpuMG/xWJJwfpkvwqWQwLIo9FK/Z3NQu/lwsthK7YK0qSnMrFYcgLK8Qe561tQw8osVLmrTiSsIgi7HGzFhuOjdEGll9JxeZ/JXrW/EXRBKiowsOHyt3TPBEnr2pVj2ldV0GRdP8thHQXArlBSOcGWMGifTnvTLPyWSJHjYVpER12/kfhtO3WOj7lmdellHluRDNv4IVpfkujV00aaSobWHzRIvl+5ytB7K9Y6he/Z9prXt89NlqDQIwqmipN5v4ftw5C0Ba6J9kEwFE3YeBRwWuHbA06BztwsHZpAZyV4crRBL0QZzkGsy294XtwExt/Tg2QH92Fh3uErHv1gKC+cxAR2VnzsOChCucV/TaHQTpguokcCod8n36YSZRxCLIDOFmxlIkj61q91zA5blUJqrTusNOm0laljuYmxm5ehFFE3eqw6PN4JbvnxvTB0DJ/UXejcdJxuSgm+z8/OaVGEt4uEKmo4w/5jweT1uMYDzV6KNqVc2BpGg1cefUgKVGhRfwrsaHWcA35tKWDiERfsIWJBPl3vz2oAlfmLV3sii0uNufeV6WoQDGs9eijYGroO8m9ZLEcHlWwm5uSl3HM/0EAzCQ8bqRfqHX3i74mwfon8J74TcuOHucNkUNezSkbofy43lMvyBGFGi3Q1r8IeqolMcAm0wMOdqA1A1vIV/GgUktCVpQPCK0Njs+256nNG99qzwMRHcEtVK5raMbx6BU4CwOem65t+IF9r6XxeHAQs/HUPp6/wCLwARW0L7RXey7g7x/YTDNeTC1JsH761LtezDO2bIxciagAwv8ZMLQ/eQxJqLij1/mgJlFVtW2QTmDaIOH2KXCE/qOLf4oU3bmzcTjjUUlH77+/8GvhNMlBBKJWavX+Np06K6RX9M2BwLRJ/pAHFUOzLD4N23cVdvh2FeSHpQ+hIoDKvQFx8Qwdnc9vrov20460o+MHq47lp8BymNhdEfZ05C40eAfWCwmDyZa4QAQ03fGkZyuGAH8Eg2I5ekYQ00euIJBJfawqr6CVUN7b805hn3/Lg5zSsK9Juk9SY2sfz/JeRdR+x+kqXvMVxtI8UrrV9sR6FomrhUYehVDrPLLpnmQDtGHE/YuMFYn/YPEzUSnge0KSeWh8M24qj9fQpx+v3m8ghjJvkQsQFrnhGbNL4TTtXcxE9aFzu+fO7HyXdzttmmHD0LYPh4nfjWe7kQOJasU4T3L760=", it: 310000 };
  var LS = "gx-lock156";
  function b64(s) { var b = atob(s), u = new Uint8Array(b.length); for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
  function imp(pk) { return crypto.subtle.importKey("pkcs8", pk, { name: "RSA-OAEP", hash: "SHA-256" }, false, ["decrypt"]); }
  function tryPw(pw) {
    return crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveKey"]).then(function (base) {
      return crypto.subtle.deriveKey({ name: "PBKDF2", salt: b64(W.salt), iterations: W.it, hash: "SHA-256" }, base, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
    }).then(function (ak) {
      return crypto.subtle.decrypt({ name: "AES-GCM", iv: b64(W.iv) }, ak, b64(W.wk));
    }).then(function (buf) {
      var pk = new Uint8Array(buf), s = "";
      for (var i = 0; i < pk.length; i++) s += String.fromCharCode(pk[i]);
      try { localStorage.setItem(LS, btoa(s)); } catch (e) {}
      return imp(pk);
    });
  }
  function onBody(f) { if (document.body) f(); else document.addEventListener("DOMContentLoaded", f); }
  function show(done) {
    onBody(function () {
      var d = document.createElement("div");
      d.id = "gx-lock156";
      d.setAttribute("style", "position:fixed;inset:0;z-index:99999;background:#121212;color:#fafafa;display:flex;align-items:center;justify-content:center;padding:24px;font-family:Inter,system-ui,-apple-system,sans-serif");
      d.innerHTML = '<form style="width:100%;max-width:320px;text-align:center"><img src="icon.png" alt="" style="width:56px;height:56px;border-radius:12px;margin:0 auto 14px;display:block"><div style="font-size:20px;font-weight:600;margin-bottom:6px">Fantasy Islands GM</div><div style="font-size:14px;color:#8f8f8f;margin-bottom:18px">Enter the password to open the app.</div><input type="password" autocomplete="current-password" placeholder="Password" style="width:100%;box-sizing:border-box;padding:12px 14px;border-radius:10px;border:1px solid #363636;background:#1a1a1a;color:#fafafa;font-size:16px;outline:none"><button type="submit" style="width:100%;margin-top:12px;padding:12px;border-radius:10px;border:0;background:#8b7cff;color:#fff;font-size:16px;font-weight:600">Unlock</button><div class="er" style="min-height:20px;margin-top:10px;font-size:14px;color:#f06a6a"></div></form>';
      document.body.appendChild(d);
      var f = d.querySelector("form"), inp = d.querySelector("input"), er = d.querySelector(".er"), bt = d.querySelector("button");
      setTimeout(function () { try { inp.focus(); } catch (e) {} }, 50);
      f.addEventListener("submit", function (ev) {
        ev.preventDefault();
        er.textContent = ""; bt.disabled = true; bt.textContent = "Checking...";
        tryPw(inp.value.trim()).then(function (k) { d.remove(); done(k); }, function () { bt.disabled = false; bt.textContent = "Unlock"; er.textContent = "Wrong password. Try again."; inp.select(); });
      });
    });
  }
  var unlocked = new Promise(function (res) {
    var s = null;
    try { s = localStorage.getItem(LS); } catch (e) {}
    if (!s) { show(res); return; }
    imp(b64(s)).then(res, function () { try { localStorage.removeItem(LS); } catch (e) {} show(res); });
  });
  function chacha(key, nonce, data) {
    var kv = new DataView(key.buffer, key.byteOffset, 32), nv = new DataView(nonce.buffer, nonce.byteOffset, 12);
    var st = new Uint32Array(16), x = new Uint32Array(16), ks = new Uint8Array(64), kd = new DataView(ks.buffer), out = new Uint8Array(data.length);
    st[0] = 0x61707865; st[1] = 0x3320646e; st[2] = 0x79622d32; st[3] = 0x6b206574;
    for (var i = 0; i < 8; i++) st[4 + i] = kv.getUint32(i * 4, true);
    for (i = 0; i < 3; i++) st[13 + i] = nv.getUint32(i * 4, true);
    function q(a, b, c, d) {
      x[a] += x[b]; x[d] ^= x[a]; x[d] = (x[d] << 16) | (x[d] >>> 16);
      x[c] += x[d]; x[b] ^= x[c]; x[b] = (x[b] << 12) | (x[b] >>> 20);
      x[a] += x[b]; x[d] ^= x[a]; x[d] = (x[d] << 8) | (x[d] >>> 24);
      x[c] += x[d]; x[b] ^= x[c]; x[b] = (x[b] << 7) | (x[b] >>> 25);
    }
    for (var pos = 0, ctr = 1; pos < data.length; pos += 64, ctr++) {
      st[12] = ctr; x.set(st);
      for (var r = 0; r < 10; r++) { q(0, 4, 8, 12); q(1, 5, 9, 13); q(2, 6, 10, 14); q(3, 7, 11, 15); q(0, 5, 10, 15); q(1, 6, 11, 12); q(2, 7, 8, 13); q(3, 4, 9, 14); }
      for (i = 0; i < 16; i++) kd.setUint32(i * 4, (x[i] + st[i]) >>> 0, true);
      for (var j = 0; j < 64 && pos + j < data.length; j++) out[pos + j] = data[pos + j] ^ ks[j];
    }
    return out;
  }
  function dec(E) {
    return unlocked.then(function (k) {
      return crypto.subtle.decrypt({ name: "RSA-OAEP" }, k, b64(E.k));
    }).then(function (raw) {
      var z = chacha(new Uint8Array(raw), b64(E.n), b64(E.c));
      return new Response(new Blob([z]).stream().pipeThrough(new DecompressionStream("deflate"))).text();
    }).then(function (t) { return JSON.parse(t); });
  }
  function load(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = function () { s.remove(); res(); };
      s.onerror = function () { s.remove(); rej(new Error("could not load " + src)); };
      (document.head || document.documentElement).appendChild(s);
    });
  }
  window.gxUnlocked156 = unlocked;
  window.gxLoadData156 = function () {
    return unlocked.then(function () {
      window.ESPN_ENC = null;
      return load("espn-data.enc.js?t=" + Date.now()).then(function () {
        if (!window.ESPN_ENC) throw new Error("no data");
        return dec(window.ESPN_ENC);
      });
    }).then(function (d) { window.ESPN_DATA = d; return d; });
  };
  window.gxLock156 = function () { try { localStorage.removeItem(LS); } catch (e) {} location.reload(); };
  var me = document.currentScript;
  if (me && me.getAttribute("data-boot")) {
    window.ESPN_DATA = null;
    window.gxLoadData156().catch(function (e) { console.warn("league data:", e); }).then(function () {
      window.__gxReady156 = true;
      if (window.__gxBoot156) window.__gxBoot156();
    });
  }
})();
