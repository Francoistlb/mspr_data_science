import os
import sys

# Ajouter le dossier scripts au PYTHONPATH
scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.append(scripts_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py [etl|dashboard|analysis|importCovid|importMpox]")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "etl":
        import etl_script
        etl_script.main()
    elif command == "dashboard":
        import dashboard
        dashboard.app.run(debug=False, host='127.0.0.1', port=8050, use_reloader=False)
    elif command == "analysis":
        import start_analysis
        start_analysis.main()
    elif command == "importCovid":
        import import_db
        import_db.main()
    elif command == "importMpox":
        import import_db
        import_db.main()
    else:
        print("Commande non reconnue. Utilisez 'etl', 'dashboard', 'analysis' ou 'importCovid'")
        sys.exit(1)