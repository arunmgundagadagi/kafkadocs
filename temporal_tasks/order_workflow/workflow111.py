from temporalio import workflow
from actiivties import validate_order ,charge_payment, send_confirmation
from datetime import timedelta

@workflow.defn
class OrderWorkflow:
#    def __init__(self):
        # flag for cancle 
 #       self.is_cancelled = False
    @workflow.run
    async def run(self, order_id: str, amount: float):
        print(f"Starting workflow for order {order_id}")
        
 #       if self.is_cancelled:
 ##          return "Order Cancelled"  
        
        is_valid = await workflow.execute_activity(
                validate_order,
                order_id,
                schedule_to_close_timeout=timedelta(seconds=5),
            )
        
        if not is_valid:
                raise Exception("Order validation failed")
        
#        if self.is_cancelled:
 #           print(f"Order {order_id} cancelled before payment.")
  #          return "Order Cancelled"  
             
        payment_result = await workflow.execute_activity(
                charge_payment,
                args=(order_id, amount),
                schedule_to_close_timeout=timedelta(seconds=5),
            )
        print(payment_result)

 #       if self.is_cancelled:
  #          print(f"Order {order_id} cancelled before sending confirmation.")
    #        return "Order Cancelled"
        
        email_result = await workflow.execute_activity(
                send_confirmation,
                order_id,
                schedule_to_close_timeout=timedelta(seconds=5),
            )
        print(email_result)
            
        print(f"Workflow for order {order_id} completed")

        return "workflow execution completed "
    
#    @workflow.signal
#    async def cancel_order(self):
#        
 #       self.is_cancelled = True
 #       print("Cancel signal received. Order will be cancelled.")    
                                                                        #if __name__ == "__main__":
                                                                            # Start your workflow or other initialization code here
                                                                        # workflow_instance = OrderWorkflow()**    