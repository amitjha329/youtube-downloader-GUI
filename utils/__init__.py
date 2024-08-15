def bytes_to_mibs(bytes_per_second:int):
  """Converts bytes per second to mebibytes per second.

  Args:
    bytes_per_second: The data transfer rate in bytes per second.

  Returns:
    The data transfer rate in mebibytes per second.
  """

  mibs = bytes_per_second / (1024 * 1024)
  return round(mibs,2)