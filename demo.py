"""
GearGuard+ Demo Script
Demonstrates key features and workflows
"""
import sys
import io

# Fix encoding for Windows terminal
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from app import GearGuardApp
from datetime import datetime, timedelta


def demo_workflow():
    """Demonstrate complete maintenance workflow"""
    app = GearGuardApp()
    
    print("=" * 70)
    print("GEARGUARD+ MAINTENANCE MANAGEMENT SYSTEM - DEMO")
    print("=" * 70)
    print()
    
    # Setup demo data
    print("📦 Setting up demo data...")
    demo_data = app.setup_demo_data()
    print("✅ Demo data created\n")
    
    # Get equipment
    equipment_model = app.env['equipment']
    equipments = equipment_model.search([])
    
    if equipments:
        equip = equipments[0]
        equip_id = equip['id']
        equip_name = equip['name']
        
        print(f"🔧 Equipment: {equip_name}")
        print(f"   Initial Health Score: {equip.get('health_score', 100)}/100")
        print()
        
        # Create a corrective maintenance request
        print("📝 Creating corrective maintenance request...")
        request_model = app.env['maintenance.request']
        
        # Create request with past scheduled date to demonstrate overdue
        past_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        request = request_model.create({
            'subject': 'Emergency repair needed',
            'equipment_id': equip_id,
            'request_type': 'corrective',
            'scheduled_date': past_date,
            'description': 'Equipment malfunction detected',
        })
        
        request_id = request._records[-1]['id']
        print(f"✅ Request created (ID: {request_id})")
        print(f"   State: {request._records[-1]['state']}")
        print(f"   Overdue: {request._records[-1].get('is_overdue', False)}")
        print()
        
        # Check health score after creating request
        equipment_model._compute_health_score(equip_id)
        updated_equip = equipment_model.browse([equip_id])[0]
        print(f"📊 Updated Health Score: {updated_equip.get('health_score', 100)}/100")
        print()
        
        # Start maintenance
        print("▶️  Starting maintenance...")
        request_model.action_start(request_id)
        updated_request = request_model.browse([request_id])[0]
        print(f"✅ State changed to: {updated_request['state']}")
        print()
        
        # Complete repair
        print("✅ Completing repair with duration...")
        try:
            request_model.action_repair(request_id, duration=3.5)
            completed_request = request_model.browse([request_id])[0]
            print(f"✅ Request completed!")
            print(f"   Final State: {completed_request['state']}")
            print(f"   Duration: {completed_request.get('duration', 0)} hours")
            print()
            
            # Check health score after repair
            equipment_model._compute_health_score(equip_id)
            final_equip = equipment_model.browse([equip_id])[0]
            print(f"📊 Final Health Score: {final_equip.get('health_score', 100)}/100")
            print()
        except ValueError as e:
            print(f"❌ Error: {e}")
            print()
    
    # Display dashboard
    print("=" * 70)
    print("DASHBOARD ANALYTICS")
    print("=" * 70)
    print()
    
    dashboard_data = app.get_dashboard_data()
    
    # KPIs
    kpis = dashboard_data['kpis']
    print("📊 Key Performance Indicators:")
    print(f"   Total Equipment: {kpis['total_equipment']}")
    print(f"   Open Requests: {kpis['open_requests']}")
    print(f"   Overdue Requests: {kpis['overdue_requests']}")
    print(f"   Critical Health Equipment: {kpis['critical_equipment']}")
    print()
    
    # Preventive vs Corrective
    pvc = dashboard_data['preventive_vs_corrective']
    total = pvc['preventive'] + pvc['corrective']
    if total > 0:
        preventive_pct = (pvc['preventive'] / total) * 100
        corrective_pct = (pvc['corrective'] / total) * 100
        print("📈 Maintenance Type Distribution:")
        print(f"   Preventive: {pvc['preventive']} ({preventive_pct:.1f}%)")
        print(f"   Corrective: {pvc['corrective']} ({corrective_pct:.1f}%)")
        print()
    
    # Requests per team
    print("👥 Requests per Team:")
    for team_data in dashboard_data['requests_per_team']:
        print(f"   {team_data['team_name']}: {team_data['request_count']} requests")
    print()
    
    # Technician workloads
    print("⚖️  Technician Workload Balancing:")
    workloads = dashboard_data['technician_workloads']
    for workload in workloads:
        status = "🔴 High" if workload['workload'] > 5 else "🟡 Medium" if workload['workload'] > 3 else "🟢 Low"
        print(f"   {workload['technician_name']}: {workload['workload']} open tasks {status}")
    print()
    
    # Predictive alerts
    print("⚠️  Predictive Maintenance Alerts:")
    alerts = dashboard_data['alerts']
    if alerts:
        for alert in alerts:
            severity_icon = "🔴" if alert['severity'] == 'critical' else "🟡"
            print(f"   {severity_icon} {alert['equipment_name']}")
            print(f"      Health Score: {alert['health_score']}/100")
            print(f"      Breakdowns (30 days): {alert['breakdown_count']}")
            for reason in alert['reasons']:
                print(f"      • {reason}")
            print()
    else:
        print("   ✅ No alerts - all equipment operating normally")
        print()
    
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print()
    print("Key Features Demonstrated:")
    print("  ✓ Equipment health scoring")
    print("  ✓ Maintenance request workflow")
    print("  ✓ Overdue detection")
    print("  ✓ Dashboard analytics")
    print("  ✓ Predictive alerts")
    print("  ✓ Workload balancing")
    print()


if __name__ == '__main__':
    demo_workflow()

