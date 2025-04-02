from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.window import TumblingWindow

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
table_env = StreamTableEnvironment.create(environment_settings=settings)