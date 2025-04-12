import json

from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal types.

    For dealing with DynamoDB Decimal types, which are not JSON serializable.
    """

    def default(self, obj):
        """Convert Decimal to int or float.

        Args:
            obj: The object to convert.

        Returns:
            int or float: The converted value.
        """
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)
