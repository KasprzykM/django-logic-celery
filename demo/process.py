from django_logic import Process, Transition
from django_logic_celery import SideEffectTasks, CallbacksTasks


class InProgressTransition(Transition):
    side_effects = SideEffectTasks()


class ProgressTransition(Transition):
    side_effects = SideEffectTasks()
    callbacks = CallbacksTasks()
    failure_callbacks = CallbacksTasks()


class InvoiceProcess(Process):
    process_name = 'invoice_process'

    states = (
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    transitions = [
        Transition(
            action_name='approve',
            sources=['draft'],
            target='approved'
        ),
        InProgressTransition(
            action_name='send_to_customer',
            sources=['approved'],
            side_effects=['demo.tasks.send_to_a_customer'],
            target='sent'
        ),
        Transition(
            action_name='void',
            sources=['draft', 'paid'],
            target='voided'
        ),
        ProgressTransition(
            action_name='demo',
            sources=['draft'],
            target='sent',
            in_progress_state='in_progress',
            side_effects=['demo.tasks.demo_task_1', 'demo.tasks.demo_task_2', 'demo.tasks.demo_task_3'],
            callbacks=['demo.tasks.demo_task_4', 'demo.tasks.demo_task_5']
        ),
        ProgressTransition(
            action_name='failing_transition',
            sources=['draft'],
            target='sent',
            in_progress_state='in_progress',
            failed_state='failed',
            side_effects=['demo.tasks.demo_task_1', 'demo.tasks.demo_task_exception', 'demo.tasks.demo_task_2'],
            failure_callbacks=['demo.tasks.demo_task_3', 'demo.tasks.demo_task_4']
        )

    ]