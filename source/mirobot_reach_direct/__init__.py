def _register_isaaclab_tasks() -> None:
    import gymnasium as gym

    from . import agents
    from .mirobot_reach_env import MirobotReachPregraspEnvCfg

    gym.register(
        id="Mirobot-Reach-Pregrasp-Direct-v0",
        entry_point=f"{__name__}.mirobot_reach_env:MirobotReachPregraspEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": MirobotReachPregraspEnvCfg,
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MirobotReachPPORunnerCfg",
        },
    )


try:
    _register_isaaclab_tasks()
except ModuleNotFoundError as exc:
    if exc.name not in {"gymnasium", "isaaclab", "pxr"}:
        raise
