def _register_isaaclab_tasks() -> None:
    import gymnasium as gym

    from . import agents
    from .mirobot_reach_env import MirobotReachPregraspEnvCfg
    from .mirobot_mars_twin_env import (
        MirobotMarsTwinPickEnvCfg,
        MirobotMarsTwinPlaceEnvCfg,
        MirobotMarsTwinPullEnvCfg,
        MirobotMarsTwinPushEnvCfg,
        MirobotMarsTwinStackEnvCfg,
    )

    gym.register(
        id="Mirobot-Reach-Pregrasp-Direct-v0",
        entry_point=f"{__name__}.mirobot_reach_env:MirobotReachPregraspEnv",
        disable_env_checker=True,
        kwargs={
            "env_cfg_entry_point": MirobotReachPregraspEnvCfg,
            "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MirobotReachPPORunnerCfg",
        },
    )

    mars_twin_tasks = {
        "Mirobot-Mars-Twin-Pick-Direct-v0": MirobotMarsTwinPickEnvCfg,
        "Mirobot-Mars-Twin-Place-Direct-v0": MirobotMarsTwinPlaceEnvCfg,
        "Mirobot-Mars-Twin-Stack-Direct-v0": MirobotMarsTwinStackEnvCfg,
        "Mirobot-Mars-Twin-Push-Direct-v0": MirobotMarsTwinPushEnvCfg,
        "Mirobot-Mars-Twin-Pull-Direct-v0": MirobotMarsTwinPullEnvCfg,
    }
    for task_id, cfg_cls in mars_twin_tasks.items():
        gym.register(
            id=task_id,
            entry_point=f"{__name__}.mirobot_mars_twin_env:MirobotMarsTwinEnv",
            disable_env_checker=True,
            kwargs={
                "env_cfg_entry_point": cfg_cls,
                "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MirobotMarsTwinPPORunnerCfg",
            },
        )


try:
    _register_isaaclab_tasks()
except ModuleNotFoundError as exc:
    if exc.name not in {"gymnasium", "isaaclab", "pxr"}:
        raise
