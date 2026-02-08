"""Performance test script for CLI Todo application."""

import time

from src.services.task_service import TaskService


def test_performance_with_100_tasks():
    """Test performance with 100 tasks."""
    service = TaskService()

    # Test 1: Add 100 tasks
    start = time.time()
    for i in range(100):
        service.add_task(f"Task {i+1}")
    add_time = time.time() - start
    print(f"✓ Added 100 tasks in {add_time:.4f} seconds")
    assert add_time < 1.0, f"Adding 100 tasks took {add_time:.4f}s (should be <1s)"

    # Test 2: List all 100 tasks
    start = time.time()
    tasks = service.get_all_tasks()
    list_time = time.time() - start
    print(f"✓ Listed 100 tasks in {list_time:.4f} seconds")
    assert list_time < 1.0, f"Listing 100 tasks took {list_time:.4f}s (should be <1s)"
    assert len(tasks) == 100

    # Test 3: Mark 50 tasks as complete
    start = time.time()
    for i in range(1, 51):
        service.mark_complete(i)
    complete_time = time.time() - start
    print(f"✓ Marked 50 tasks complete in {complete_time:.4f} seconds")
    assert complete_time < 1.0, f"Completing 50 tasks took {complete_time:.4f}s (should be <1s)"

    # Test 4: Update 25 tasks
    start = time.time()
    for i in range(51, 76):
        service.update_task(i, f"Updated task {i}")
    update_time = time.time() - start
    print(f"✓ Updated 25 tasks in {update_time:.4f} seconds")
    assert update_time < 1.0, f"Updating 25 tasks took {update_time:.4f}s (should be <1s)"

    # Test 5: Delete 25 tasks
    start = time.time()
    for i in range(76, 101):
        service.delete_task(i)
    delete_time = time.time() - start
    print(f"✓ Deleted 25 tasks in {delete_time:.4f} seconds")
    assert delete_time < 1.0, f"Deleting 25 tasks took {delete_time:.4f}s (should be <1s)"

    # Verify final state
    remaining_tasks = service.get_all_tasks()
    assert len(remaining_tasks) == 75
    print(f"✓ Final verification: 75 tasks remaining (correct)")

    print("\n✅ All performance tests passed!")
    print(f"   Total time: {add_time + list_time + complete_time + update_time + delete_time:.4f}s")


if __name__ == "__main__":
    test_performance_with_100_tasks()
