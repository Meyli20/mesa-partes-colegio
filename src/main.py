from utils.tramites import (
    cargar_datos_prueba,
    registrar_estudiante_menu,
    registrar_area_menu,
    buscar_por_codigo_menu,
    registrar_tramite_menu,
    atender_tramite_menu,
    buscar_areas_por_tramite_menu,
    consultar_historial_estudiante_menu,
)


def menu_principal():
    while True:
        print("\n========================================")
        print("    MESA DE PARTES - MENÚ PRINCIPAL")
        print("========================================")
        print("1. Registrar Estudiante (RF01)")
        print("2. Registrar Área (RF02)")
        print("3. Buscar por Código (RF03)")
        print("4. Registrar Trámite (RF04)")
        print("5. Atender Trámite / Cambiar Estado (RF05)")
        print("6. Buscar Áreas por Tipo de Trámite (Consulta Funcional)")
        print("7. Consultar Historial de Trámites por Estudiante")
        print("8. Salir del Sistema")

        opcion = input("\nSeleccione una opción (1-8): ").strip()

        if opcion == "1":
            registrar_estudiante_menu()
        elif opcion == "2":
            registrar_area_menu()
        elif opcion == "3":
            buscar_por_codigo_menu()
        elif opcion == "4":
            registrar_tramite_menu()
        elif opcion == "5":
            atender_tramite_menu()
        elif opcion == "6":
            buscar_areas_por_tramite_menu()
        elif opcion == "7":
            consultar_historial_estudiante_menu()
        elif opcion == "8":
            print("\nSaliendo de la mesa de partes... ¡Hasta luego!")
            break
        else:
            print("\n[!] Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    cargar_datos_prueba()
    menu_principal()
