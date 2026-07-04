# Deploy on DigitalOcean: wake up to the email

Goal: an always-on cloud computer that runs the whole pipeline every weekday
morning and emails you the report before the open. You touch nothing. Your own
laptop can be off.

Cost: about $6 per month for the smallest droplet. Gemini stays free.

Time: about 20 minutes, one time.

---

## Part 1: Create the droplet (in the DigitalOcean website)

1. Go to digitalocean.com and make an account. New accounts usually get free
   trial credit, so the first couple of months can be $0.
2. Top right, click **Create** then **Droplets**.
3. Choose these options:
   - **Region:** pick New York (closest to the US market data and your ET
     timezone).
   - **OS image:** Ubuntu, the latest LTS version (24.04 or newer).
   - **Droplet type:** Basic.
   - **CPU:** Regular, the cheapest one (1 GB RAM / 1 CPU, about $6/mo). Plenty
     for this.
   - **Authentication:** choose **Password** (simplest) and set a strong root
     password. Write it down. (SSH keys are more secure if you know them, but
     password is fine to start.)
4. Click **Create Droplet**. Wait about a minute until it shows an IP address
   like `164.92.x.x`. Copy that IP.

---

## Part 2: Connect to the droplet

From your Windows PC, open PowerShell and connect (replace the IP with yours):

```powershell
ssh root@164.92.x.x
```

Say `yes` to the fingerprint question, then paste the root password you set
(the cursor will not move while you type the password, that is normal). You are
now typing commands ON the droplet, not your PC.

Everything from here runs on the droplet.

---

## Part 3: Install the tools on the droplet

Paste these one block at a time.

```bash
apt update && apt install -y python3-venv python3-pip git curl
```

Install Node (needed for the Claude Code CLI):

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt install -y nodejs
```

Install Claude Code:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

If `claude` is not found after that, add it to the path for this session:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Part 4: Get the project

```bash
git clone https://github.com/jrrodrz1620/https-github.com-TradersPost-pinescript-agents.git
cd https-github.com-TradersPost-pinescript-agents
git checkout claude/premarket-analyst-pipeline-xrqg56
cd premarket-analyst
```

Set up the Python side:

```bash
python3 -m venv .venv
.venv/bin/pip install yfinance feedparser markdown requests
chmod +x run_morning.sh bin/grok-ask.sh
```

---

## Part 5: Log in the two brains

**Brain 1, Claude Code.** Run:

```bash
claude
```

It prints a login URL. Copy that URL, open it in your PC browser, sign in with
your Claude Pro account, and paste the code back. Then type `/exit` to leave.
This logs the droplet in once, it stays logged in.

**Brain 2, Gemini.** Create your `.env` and add the keys:

```bash
cp .env.example .env
nano .env
```

In the nano editor, fill in these lines (arrow keys to move, just type the
values):

```
RESEND_API_KEY=re_your_resend_key
EMAIL_TO=rod440020@gmail.com
SECOND_BRAIN_URL=https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
SECOND_BRAIN_MODEL=gemini-2.5-flash
SECOND_BRAIN_KEY=your_gemini_key
```

Save and exit nano: press **Ctrl+O**, then **Enter**, then **Ctrl+X**.

---

## Part 6: Test the whole thing by hand

```bash
./run_morning.sh
```

Watch the log. It should walk through 1/6 scan to 6/6 deliver, and the report
lands in your Gmail. If a step warns or fails, the log says which one, and you
can fix just that piece (usually a key typo in `.env`, reopen with `nano .env`).

Note: on a weekend or holiday the gappers and econ calendar may be empty or
thin. That is correct, not a bug. The real test is a weekday.

---

## Part 7: Schedule it to run every morning

Open the scheduler:

```bash
crontab -e
```

(If it asks which editor, pick nano, usually option 1.)

Add these two lines at the bottom. Replace the path if your clone landed
somewhere else (run `pwd` to check where you are):

```cron
CRON_TZ=America/New_York
30 8 * * 1-5 /root/https-github.com-TradersPost-pinescript-agents/premarket-analyst/run_morning.sh >> /root/premarket.log 2>&1
```

Save and exit (Ctrl+O, Enter, Ctrl+X).

That means: 8:30am ET, Monday through Friday, run the pipeline and append the
output to `premarket.log`. Done. From tomorrow on the report just shows up in
your inbox.

---

## Everyday life after setup

- **You do nothing.** The email arrives each weekday around 8:35am ET.
- **Check what happened:** `ssh root@your-ip` then `cat premarket.log`.
- **Change a rule or prompt:** edit the file, or on your PC push a change and
  on the droplet run `git pull`.
- **Pause it:** `crontab -e`, put a `#` in front of the schedule line.
- **Turn off the machine to stop billing:** destroy the droplet in the
  DigitalOcean site (your code is safe on GitHub, just redo Parts 1 to 7 to
  bring it back).

## When something looks off in the report

The pipeline is decision support, not signals. If a morning looks wrong (a
catalyst mismatch, a thin list), read `premarket.log` to see which brain said
what. The rules pick the names, the two brains judge them, you make the trade.
