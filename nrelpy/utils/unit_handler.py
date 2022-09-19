from unyt import MW, kW, W, GW, hr, day, year
from unyt import unyt_quantity

_unit_dict = {"$/kW":kW**-1,
                "$/MW":MW**-1,
                "$/GW":GW**-1,
                "$/W":W**-1}

def tuple_to_quantity(quantity_tuple: tuple[float, str],
                        to_unit: str) -> unyt_quantity:
    """
    Converts a value unit tuple to a :class:`unyt_quantity`.

    Parameters
    ----------
    quantity_tuple : tuple
        A tuple with two entries, `value` [float] and `unit` [str].
    value : string, float, int
        The magnitude of the quantity.
    unit : string, :class:`unyt.unit_object`
        The desired unit for the quantity.
    """

