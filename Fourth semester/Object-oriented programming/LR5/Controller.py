from typing import Dict, Any, List
from Factory import LogisticsFactory
from ShipmentBuilder import ShipmentBuilder


class LogisticsController:
    """
    GRASP Controller: Обрабатывает системные события (запрос на доставку).
    """

    def __init__(self, factory: LogisticsFactory):
        self.__factory = factory

    def process_request(self, cargo_requests: List[Dict[str, Any]],
                        distance: float,
                        transport_type: str) -> Dict[str, Any]:
        try:
            builder = ShipmentBuilder(self.__factory)

            for request in cargo_requests:
                builder.add_cargo(request["type"], request["qty"])

            builder.set_distance(distance)
            builder.set_transport(transport_type)

            shipment = builder.build()

            return {
                "success": True,
                "total_mass": shipment.calculate_total_mass(),
                "total_cost": shipment.calculate_delivery_cost(),
                "time_hours": shipment.calculate_delivery_time(),
                "transport": shipment.get_transport_name(),
                "distance": shipment.get_distance()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }