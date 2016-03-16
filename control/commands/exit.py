import cloud_interface.file_tree_navigation.structure_fetcher as sf


def handler(user_input):
    """
    Tear-down function.
    Args:
        user_input: The arguments provided by the user.

    Returns: None
    """
    # Save metadata.
    print "Saving meta-data."
    sf.save_metadata()
    print "Session ended."
    exit(0)
