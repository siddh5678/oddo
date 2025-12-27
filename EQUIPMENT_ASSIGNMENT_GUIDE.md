# Equipment Assignment Guide

## 🔧 Equipment में Assignments

Equipment में दो तरह के assignments होते हैं:

### 1. **Assigned Employee (Equipment Operator)**
**यह कौन है?**
- वो employee जो equipment को **daily use करता है** या **operate करता है**
- Equipment का **primary user/operator**
- Equipment के लिए **responsible person**

**Examples:**
- Production Line Operator
- Machine Operator  
- Facility Manager
- Department Head
- Equipment User

**Important:**
- यह **maintenance technician नहीं है**
- यह **equipment का user/operator है**
- Optional field है (required नहीं)

### 2. **Maintenance Team**
**यह क्या है?**
- वो team जो equipment का **maintenance करेगी**
- Equipment repair और maintenance के लिए **responsible team**
- Maintenance requests automatically इस team को assign होंगी

**Examples:**
- Electrical Team
- Mechanical Team
- HVAC Team

**Important:**
- यह **required है** (maintenance के लिए)
- Request create करते समय automatically assign होती है

## 📊 Difference

| Field | Purpose | Who? | Required? |
|-------|---------|------|-----------|
| **Assigned Employee** | Equipment Operator | जो equipment use करता है | Optional |
| **Maintenance Team** | Maintenance Team | जो equipment repair करेगी | Required |

## 🎯 Real-World Example

**Example: Production Conveyor Belt**

1. **Assigned Employee:**
   - Name: "Mike Operator"
   - Role: Production Line Operator
   - Responsibility: Daily operation of conveyor belt

2. **Maintenance Team:**
   - Name: "Electrical Team"
   - Responsibility: Maintenance and repairs

**Flow:**
- Mike Operator daily conveyor belt चलाता है
- अगर problem आती है, Mike maintenance request create करता है
- Request automatically "Electrical Team" को assign हो जाती है
- Team का technician repair करता है

## 💡 When to Assign Employee?

**Assign करें जब:**
- Equipment का primary operator known है
- Specific person equipment के लिए responsible है
- Contact person की जरूरत है
- Equipment usage tracking करना है

**Assign न करें जब:**
- Equipment shared है (multiple operators)
- Operator unknown है
- Not applicable है

## 🔄 Complete Flow

```
Equipment Creation
    ↓
[Assign Maintenance Team] ← Required for maintenance
    ↓
[Assign Employee/Operator] ← Optional, for tracking
    ↓
Equipment Saved
    ↓
Maintenance Request Created
    ↓
Team Auto-Assigned ✅
    ↓
Technician Selected (from team)
    ↓
Request Assigned
```

## ❓ Common Questions

**Q: Assigned Employee technician हो सकता है?**
A: हाँ, लेकिन usually यह operator/user होता है। Technician maintenance request में assign होता है।

**Q: दोनों same person हो सकते हैं?**
A: हाँ, possible है। लेकिन usually:
- Employee = Operator (daily use)
- Technician = Maintenance person (repair)

**Q: Assigned Employee required है?**
A: नहीं, यह optional field है। Maintenance Team required है।

**Q: Maintenance Team के बिना equipment create कर सकते हैं?**
A: Technically हाँ, लेकिन maintenance requests के लिए team assign करना better है।

## 📝 Best Practices

1. **Always assign Maintenance Team** - Maintenance के लिए जरूरी
2. **Assign Employee if known** - Better tracking के लिए
3. **Keep them separate** - Operator ≠ Technician
4. **Update when needed** - Employee change होने पर update करें

