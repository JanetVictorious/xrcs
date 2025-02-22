::: src.screens.main_screen.MainScreen
    options:
        show_root_heading: true
        merge_init_into_class: false
        group_by_category: false
        members:
          - __init__


::: src.screens.profile_screen.ProfileScreen
    options:
        show_root_heading: true
        merge_init_into_class: false
        group_by_category: false
        members:
          - __init__
          - save_profile

::: src.screens.workout_list_screen.WorkoutListScreen
    options:
        show_root_heading: true
        merge_init_into_class: false
        group_by_category: false
        members:
          - __init__
          - create_workout_item
          - refresh_workouts

::: src.screens.workout_planning_screen.WorkoutPlanningScreen
    options:
        show_root_heading: true
        merge_init_into_class: false
        group_by_category: false
        members:
          - __init__
          - add_exercise_input
          - remove_row
          - save_workout
          - clear_inputs
