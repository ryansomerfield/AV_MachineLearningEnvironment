from gym.envs.registration import register

register(id='DIYRobocarEnv-v0',
    entry_point='envs.DIYRobocar_env_dir:DIYRobocarEnv'
)