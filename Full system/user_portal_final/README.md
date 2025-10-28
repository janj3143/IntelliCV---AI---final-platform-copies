# 🚀 IntelliCV-AI Portal Launcher Guide

Welcome to your local IntelliCV-AI development environment! This guide will help you run all three portals in VS Code.

## 🎯 Portal Overview

You now have **three different portal versions** with updated pricing and 2FA security:

| Portal | Port | Description | Features |
|--------|------|-------------|----------|
| **🏆 Professional Pro** | 8503 | Comprehensive feature set | Full functionality, 2FA options |
| **⚡ Simple Start** | 8504 | Streamlined experience | Quick access, simplified 2FA |
| **🚀 Backup Recovered** | 8508 | Advanced admin integration | Complete 2FA, admin AI, enterprise features |

## 💰 New Pricing Structure

All portals now feature your updated pricing:

- **🆓 Free Starter** - $0 (Partner-supported, limited use)
- **💎 Monthly Pro** - **$15.99** (NEW PRICE!)
- **🏆 Annual Pro** - $149.99 (Save $42!)
- **👑 Enterprise Premium** - $299.99 (All bells and whistles!)

## 🛡️ 2FA Security Features

- **Backup Recovered**: Full 2FA with QR codes, authenticator app support
- **Professional Pro**: 2FA security options with verification
- **Simple Start**: Simplified 2FA with quick verification

## 🔧 Setup Instructions

### Step 1: Install Python (if needed)

**Option A: Microsoft Store (Recommended)**
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click Install

**Option B: Python.org**
1. Go to https://python.org/downloads
2. Download Python 3.11 or 3.12
3. Run installer and **check "Add Python to PATH"**

### Step 2: Verify Installation

Open VS Code Terminal (Ctrl+`) and run:
```bash
python --version
pip --version
```

### Step 3: Install Streamlit

In VS Code Terminal:
```bash
pip install streamlit
```

## 🚀 Running the Portals

### Method 1: Run All Portals at Once

**Windows (Batch):**
```bash
.\START_ALL_PORTALS.bat
```

**PowerShell:**
```bash
.\START_ALL_PORTALS.ps1
```

### Method 2: Run Individual Portals

**Professional Pro Portal:**
```bash
.\START_PRO_PORTAL.bat
# or manually:
cd pages_pro
streamlit run 00_Welcome.py --server.port 8503
```

**Simple Start Portal:**
```bash
.\START_SIMPLE_PORTAL.bat
# or manually:
cd pages_simple
streamlit run 00_Welcome.py --server.port 8504
```

**Backup Recovered Portal:**
```bash
.\START_BACKUP_PORTAL.bat
# or manually:
cd pages_backup_recovered
streamlit run 00_Welcome.py --server.port 8508
```

### Method 3: VS Code Terminal (Manual)

Open multiple terminals in VS Code (Ctrl+Shift+`) and run:

**Terminal 1:**
```bash
cd pages_pro
streamlit run 00_Welcome.py --server.port 8503
```

**Terminal 2:**
```bash
cd pages_simple
streamlit run 00_Welcome.py --server.port 8504
```

**Terminal 3:**
```bash
cd pages_backup_recovered
streamlit run 00_Welcome.py --server.port 8508
```

## 🌐 Portal URLs

Once running, visit these URLs in your browser:

- **🏆 Professional Pro**: http://localhost:8503
- **⚡ Simple Start**: http://localhost:8504
- **🚀 Backup Recovered**: http://localhost:8508

## 🧪 Testing Features

### Demo Accounts for 2FA Testing

Use these accounts to test the enhanced security features:

| Account | Email | Password | 2FA | Subscription |
|---------|--------|----------|-----|--------------|
| Free User | demo@intellicv.ai | demo123 | No | Free |
| Pro User | pro@intellicv.ai | pro123 | Yes | Monthly |
| Admin User | admin@intellicv.ai | admin123 | Yes | Enterprise |

**2FA Demo Codes**: `123456` or `000000`

### Features to Compare

1. **Welcome Page Pricing**
   - Check all four pricing tiers
   - Compare feature lists
   - Test plan selection

2. **Login Experience**
   - Standard vs 2FA login
   - Security recommendations
   - Different user flows

3. **Registration Process**
   - 2FA setup during registration
   - Plan selection integration
   - Security options

4. **Advanced Features** (Backup Recovered)
   - Admin AI integration
   - QR code 2FA setup
   - Enterprise-grade features

## 🛠️ Troubleshooting

### Common Issues

**Python not found:**
- Restart VS Code after installing Python
- Check that Python is in your PATH
- Try `py` command instead of `python`

**Streamlit not found:**
- Make sure pip install completed successfully
- Try: `python -m pip install streamlit`

**Port already in use:**
- Close other applications using ports 8503, 8504, 8508
- Or change ports in the startup scripts

**Import errors:**
- Some advanced features may show warnings
- Basic functionality will still work
- Install missing packages as needed

### VS Code Integration

**Terminal shortcuts:**
- `Ctrl+`` - Open terminal
- `Ctrl+Shift+`` - New terminal
- `Ctrl+Shift+5` - Split terminal

**View multiple portals:**
1. Open browser windows/tabs for each portal
2. Use VS Code's built-in browser preview
3. Arrange windows side-by-side

## 📊 Performance Notes

- Each portal runs independently
- Memory usage: ~50-100MB per portal
- Startup time: 10-15 seconds per portal
- Auto-reload on file changes

## 🛑 Stopping Portals

- **Batch files**: Close the command windows
- **VS Code terminals**: Press `Ctrl+C` in each terminal
- **PowerShell**: Close PowerShell windows

## 🔍 Development Tips

1. **File watching**: Streamlit auto-reloads on file changes
2. **Debug mode**: Add `--logger.level debug` to startup commands
3. **Network access**: Use `--server.address 0.0.0.0` for network access
4. **Cache clearing**: Use `Ctrl+Shift+R` in browser to hard refresh

## 📝 Next Steps

1. **Test all three portals** - Compare user experiences
2. **Evaluate pricing display** - Ensure all tiers show correctly
3. **Test 2FA flows** - Use demo accounts with different security levels
4. **Choose best version** - Decide which portal provides optimal UX
5. **Deploy chosen version** - Use the selected portal for production

---

**Happy Testing!** 🎉

Your three-portal comparison environment is ready. Test the different approaches and choose the best user experience for your IntelliCV-AI platform.