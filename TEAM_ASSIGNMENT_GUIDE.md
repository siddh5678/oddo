# Technical Team Assignment Guide

## 🔧 Team Assignment Flow

### 1. Equipment पर Team Assign करना

**Step 1: Equipment Create करते समय**
- Equipment form में "Maintenance Team" dropdown होता है
- वहाँ से team select करें
- यह team उस equipment के सभी maintenance requests के लिए automatically assign हो जाएगी

**Step 2: Equipment Edit करके**
- Existing equipment को edit करें
- Maintenance Team change करें
- Save करें

### 2. Automatic Team Assignment (Auto-Assignment)

जब आप **Maintenance Request** create करते हैं:

1. **Equipment select करें** → Request form में equipment choose करें
2. **Team Auto-Assign हो जाती है** → System automatically equipment की team assign कर देता है
3. **Manual Override** → अगर चाहें तो manually different team select कर सकते हैं

### 3. Technician Assignment

**Important Rule**: 
- Technician **सिर्फ उसी team का member होना चाहिए** जो request पर assign है
- अगर technician team का member नहीं है, तो error आएगा

**Flow**:
1. Equipment select करें → Team auto-assign हो जाती है
2. Technician dropdown में **सिर्फ उस team के technicians** दिखेंगे
3. Technician select करें

## 📋 Step-by-Step Process

### Scenario 1: नया Equipment Add करना

```
1. Equipment → Create New
2. Equipment details fill करें
3. "Maintenance Team" dropdown से team select करें
   (Example: "Electrical Team" या "Mechanical Team")
4. Save करें
```

### Scenario 2: Maintenance Request Create करना

```
1. Maintenance Requests → New Request
2. Equipment select करें (जिसमें team already assigned है)
3. System automatically team assign कर देगा
4. Technician dropdown में सिर्फ उस team के technicians दिखेंगे
5. Technician select करें
6. Other details fill करें
7. Save करें
```

### Scenario 3: Team Change करना

```
1. Equipment → Edit Equipment
2. Maintenance Team change करें
3. Save करें
4. Future requests इस नई team से auto-assign होंगी
```

## 🎯 Key Features

### ✅ Auto-Assignment
- Equipment पर team assign करने के बाद, सभी requests automatically उस team से assign होती हैं
- Manual intervention की जरूरत नहीं

### ✅ Validation
- Technician को team का member होना चाहिए
- System automatically validate करता है

### ✅ Team Management
- Teams में technicians add/remove कर सकते हैं
- Multiple technicians एक team में हो सकते हैं

## 🔄 Complete Workflow Example

**Example: Conveyor Belt Maintenance**

1. **Equipment Setup**:
   - Equipment: "Production Line Conveyor Belt"
   - Team: "Electrical Team" (assign करें)

2. **Request Create**:
   - Subject: "Belt replacement needed"
   - Equipment: "Production Line Conveyor Belt" (select करें)
   - **Team Auto-Assigned**: "Electrical Team" ✅
   - Technician: सिर्फ "Electrical Team" के technicians दिखेंगे
   - Technician: "John Technician" (select करें)

3. **Result**:
   - Request "Electrical Team" को assign हो गई
   - "John Technician" को assign हो गया
   - System validated किया कि John Electrical Team का member है ✅

## 📊 Team Assignment Rules

| Rule | Description |
|------|-------------|
| **Equipment → Team** | Equipment create/edit करते समय team assign करें |
| **Request → Auto Team** | Request create करते समय equipment की team automatically assign होती है |
| **Request → Manual Override** | Request form में manually team change कर सकते हैं |
| **Technician → Team Member** | Technician सिर्फ assigned team का member हो सकता है |
| **Team → Multiple Technicians** | एक team में multiple technicians हो सकते हैं |

## 🛠️ UI Locations

### Equipment Form
- **Location**: Equipment → Create/Edit
- **Field**: "Maintenance Team" dropdown
- **Action**: Team select करें

### Request Form
- **Location**: Maintenance Requests → New Request
- **Field**: "Maintenance Team" (auto-filled, editable)
- **Field**: "Technician" (filtered by team)

### Team Management
- **Location**: Teams → View Teams
- **Action**: Teams में technicians add/remove करें

## 💡 Best Practices

1. **Equipment Setup**: नया equipment add करते समय हमेशा team assign करें
2. **Team Organization**: Similar equipment को same team assign करें
3. **Technician Assignment**: Workload balance करने के लिए technicians distribute करें
4. **Team Review**: Regularly teams review करें और update करें

## 🎨 Visual Flow

```
Equipment Creation
    ↓
[Select Maintenance Team]
    ↓
Equipment Saved with Team
    ↓
Maintenance Request Created
    ↓
[Equipment Selected]
    ↓
Team Auto-Assigned from Equipment
    ↓
[Technician Selected from Team Members]
    ↓
Request Created Successfully ✅
```

## ❓ Common Questions

**Q: Equipment पर team assign नहीं की तो?**
A: Request create करते समय manually team select करनी होगी

**Q: Technician को team से remove कर दिया तो?**
A: Existing requests पर कोई effect नहीं, लेकिन नई requests में वो technician नहीं दिखेगा

**Q: Multiple teams एक equipment पर?**
A: Currently एक equipment पर एक team, लेकिन request level पर manually change कर सकते हैं

**Q: Team change करने से पुरानी requests पर effect?**
A: नहीं, सिर्फ नई requests नई team से assign होंगी

