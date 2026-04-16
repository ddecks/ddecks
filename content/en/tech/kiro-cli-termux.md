+++
title = 'Running Kiro CLI on Android with Termux'
description = 'How I got Kiro CLI authenticated on my phone, and the IPv6/rustls rabbit hole that almost stopped me'
date = 2026-04-15
tags = ['termux', 'android', 'kiro', 'cli', 'rust', 'tls', 'workaround']
weight = 1
+++

## What is Termux?

Termux is a terminal emulator and Linux environment for Android. No root required. You get a real package manager (`pkg`), a proper shell, and access to dev tools like Python, Rust, Node.js, Git, and SSH. It's a lightweight Linux distro in your pocket.

If you've ever wanted to code, manage infrastructure, or run CLI tools from your phone, Termux is how you do it.

## Why Kiro CLI on a Phone?

Sometimes you're away from your desk and need to:

- Quickly ask Kiro to generate or review a snippet
- Run an automated task via `--no-interactive` mode
- SSH into a dev box and want a local AI assistant in your terminal

Kiro CLI works great in Termux once you get past the authentication hurdle — which is what this post is about.

## The Problem

Installing Kiro CLI on Termux is straightforward, but when you try to log in:

```bash
kiro-cli login --use-device-flow
```

You hit:

```
error: dispatch failure
io error: error sending request for url (https://oidc.us-east-1.amazonaws.com/client/register)
```

The `--use-device-flow` flag is designed for headless/remote environments where a browser redirect won't work. Exactly the Termux use case. But it still fails.

Adding `--verbose` reveals two separate issues stacked on top of each other.

## Issue 1: Missing CA Certificates

```
WARN: no native root CA certificates found!
```

Kiro CLI is compiled with **rustls**, a pure-Rust TLS implementation. Unlike OpenSSL (which `curl` uses), rustls doesn't tap into the Android system certificate store. It needs to be told where the CA bundle lives.

Termux ships with CA certificates, but rustls doesn't know where to find them. The fix:

```bash
export SSL_CERT_FILE=$PREFIX/etc/tls/cert.pem
```

You can verify the file exists first:

```bash
ls $PREFIX/etc/tls/cert.pem
```

Make it permanent:

```bash
echo 'export SSL_CERT_FILE=$PREFIX/etc/tls/cert.pem' >> ~/.bashrc
```

After this, the CA warning disappears. But the connection still times out.

## Issue 2: IPv6 Resolution Failure

With the cert warning gone, the verbose output shows:

```
identity resolver timed out after 5s
error sending request for url (https://oidc.us-east-1.amazonaws.com/client/register)
```

Five seconds. That's suspiciously specific. I tested with curl:

```bash
# IPv6 — times out or fails to resolve
curl -6 -v https://oidc.us-east-1.amazonaws.com/ 2>&1 | head -10

# IPv4 — works immediately (403 is expected, it means we reached AWS)
curl -4 -v https://oidc.us-east-1.amazonaws.com/ 2>&1 | head -10
```

There it is. Kiro CLI's Rust HTTP client (hyper/tokio) attempts IPv6 first. On many mobile networks, IPv6 DNS resolution for AWS endpoints either fails silently or hangs. The client waits 5 seconds, times out, and surfaces the error as `dispatch failure`.

`curl` handles this gracefully — it falls back to IPv4 quickly. The Rust stack doesn't.

## The Fix: tinyproxy

The solution is to route traffic through a local proxy that connects over IPv4. I used **tinyproxy** — a tiny C-based HTTP proxy (~100KB) available in Termux.

```bash
pkg install tinyproxy
```

Create a minimal config:

```bash
cat > $PREFIX/etc/tinyproxy/tinyproxy.conf << 'EOF'
Port 8080
Listen 127.0.0.1
Timeout 600
Allow 127.0.0.1
ConnectPort 443
EOF
```

Start it:

```bash
tinyproxy -c $PREFIX/etc/tinyproxy/tinyproxy.conf
```

You'll see a warning about logging being deactivated — that's fine, it's running as a daemon in the background.

Now log in:

```bash
export HTTPS_PROXY=http://127.0.0.1:8080
export SSL_CERT_FILE=$PREFIX/etc/tls/cert.pem
kiro-cli login --use-device-flow
```

This time you'll see a device code and a URL. Open the URL in your phone's browser, enter the code, authenticate with Builder ID, and you're in.

## Making It Persistent

Add everything to your shell profile so it survives terminal restarts:

```bash
cat >> ~/.bashrc << 'EOF'

# Kiro CLI on Termux — fix rustls CA certs and IPv6 timeout
export SSL_CERT_FILE=$PREFIX/etc/tls/cert.pem
export HTTPS_PROXY=http://127.0.0.1:8080
if ! pgrep -x tinyproxy > /dev/null; then
    tinyproxy -c $PREFIX/etc/tinyproxy/tinyproxy.conf
fi
EOF
```

## TL;DR

```bash
# One-time setup
pkg install tinyproxy

cat > $PREFIX/etc/tinyproxy/tinyproxy.conf << 'EOF'
Port 8080
Listen 127.0.0.1
Timeout 600
Allow 127.0.0.1
ConnectPort 443
EOF

cat >> ~/.bashrc << 'EOF'
export SSL_CERT_FILE=$PREFIX/etc/tls/cert.pem
export HTTPS_PROXY=http://127.0.0.1:8080
if ! pgrep -x tinyproxy > /dev/null; then
    tinyproxy -c $PREFIX/etc/tinyproxy/tinyproxy.conf
fi
EOF

source ~/.bashrc
kiro-cli login --use-device-flow
```

## Why This Happens

Two things collide:

1. **rustls doesn't use the Android certificate store.** It looks for certs in standard Linux paths that don't exist in Termux's sandboxed environment. The `SSL_CERT_FILE` env var bridges the gap.

2. **Rust's async DNS resolver tries IPv6 first.** On mobile networks where IPv6 resolution for AWS endpoints fails silently, the 5-second timeout burns through before falling back to IPv4. tinyproxy sidesteps this by handling the outbound connection with its own resolver, which prefers IPv4.

Tools like `curl` work fine because they use OpenSSL (which integrates with Termux's cert store) and handle IPv4/IPv6 fallback more gracefully.

## Other Auth Options

If you have a **Kiro Pro** subscription, you can skip the OIDC flow entirely with an API key:

1. Sign in to [app.kiro.dev](https://app.kiro.dev) from your phone's browser
2. Navigate to **API Keys** and create one
3. Use it in Termux:

```bash
export KIRO_API_KEY=ksk_xxxxxxxx
kiro-cli chat --no-interactive "your prompt here"
```

The catch: API keys only work in `--no-interactive` mode. For interactive chat sessions, you need the browser-based auth — which means you need the tinyproxy workaround.

## What I'd Like to See

A `--prefer-ipv4` flag or smarter fallback in the Rust HTTP client would make this just work out of the box. Termux is a legitimate headless environment, and the device flow is supposed to handle exactly this case. The IPv6 timeout is the only thing standing in the way.

Until then, tinyproxy gets the job done.
