
opts = {
            "multicore" : [

                ["sf2000_tearing_fix" , "fast" , "disabled|fast|rotate"],
                ["sf2000_rgb_clock" , "9 MHz" , "6.6 MHz|9 MHz"],
                ["sf2000_h_total_len" , "477" , "444|477"],
                ["sf2000_v_total_len" , "326" , "304|326"],
                ["sf2000_scaling_mode" , "core-provided" , "stock|core-provided|full screen|square pixels|custom"],
                ["sf2000_scaling_custom" , "4:3" , "4:3|16:9|16:10|16:15|21:9|1:1|2:1|3:2|3:4|4:1|9:16|5:4|6:5|7:9|8:3|8:7|19:12|19:14|30:17|32:9"],
                ["sf2000_scaling_filtered" , "true" , "true|false"],
                ["sf2000_show_fps" , "false" , "true|false"]

            ] , 
            
            "Gearboy" : [

                ["gearboy_bootrom_dmg" , "Enabled" , "Disabled|Enabled" ],
                ["gearboy_bootrom_gbc" , "Enabled" , "Disabled|Enabled"],
                ["gearboy_mapper" , "Auto" , "Auto|ROM Only|MBC 1|MBC 2|MBC 3|MBC 5|MBC 1 Multicart"],
                ["gearboy_model" , "Auto" , "Auto|Game Boy DMG|Game Boy Advance"],
                ["gearboy_palette" , "Original" , "Original|Sharp|B/W|Autumn|Soft|Slime"],
                ["gearboy_up_down_allowed" , "Disabled" , "Disabled|Enabled"]

            ],

            "gpSP" : [

                ["gpsp_bios" , "auto" , "auto|builtin|official"],
                ["gpsp_boot_mode" , "game" , "game|bios"],
                ["gpsp_drc" , "disabled" , "disabled|enabled"],
                ["gpsp_sprlim" , "disabled" ,"disabled|enabled" ], 
                ["gpsp_rtc" , "auto" ,"disabled|enabled" ],
                ["gpsp_rumble" , "disabled" , "auto|disabled|enabled"], 
                ["gpsp_frameskip" , "auto" , "disabled|auto|auto_threshold|fixed_interval"], 
                ["gpsp_frameskip_threshold" , "33" , "15|18|21|24|27|30|33|36|39|42|45|48|51|54|57|60"], 
                ["gpsp_frameskip_interval" , "1" , "0|1|2|3|4|5|6|7|8|9|10"],
                ["gpsp_color_correction" , "disabled" , "disabled|enabled" ], 
                ["gpsp_frame_mixing" , "disabled" , "disabled|enabled"],
                ["gpsp_turbo_period" , "4" , "*4-120"]

            ],

            "QuickNES" : [

                ["quicknes_aspect_ratio_par" , "PAR" , "PAR|4:3"],
                ["quicknes_audio_eq" , "default" , "default|famicom|tv|flat|crisp|tinny"],
                ["quicknes_audio_nonlinear" , "nonlinear" , "nonlinear|linear|stereo panning"],
                ["quicknes_no_sprite_limit" , "disabled" , "disabled|enabled"],
                ["quicknes_palette" , "default" , "default|asqrealc|nintendo-vc|rgb|yuv-v3|unsaturated-final|sony-cxa2025as-us|pal|bmf-final2|bmf-final3|smooth-fbx|composite-direct-fbx|pvm-style-d93-fbx|ntsc-hardware-fbx|nes-classic-fbx-fs|nescap|wavebeam"],
                ["quicknes_turbo_enable" , "none" , "none|player 1|player 2|both"],
                ["quicknes_turbo_pulse_width" , "3" , "1|2|3|5|10|15|30|60"],
                ["quicknes_up_down_allowed" , "disabled" , "disabled|enabled"],
                ["quicknes_use_overscan_h" , "enabled" , "disabled|enabled"],
                ["quicknes_use_overscan_v" , "disabled" , "disabled|enabled"]


            ],

            "RACE" : [

                ["race_dark_filter_level" , "0" ,"0|5|10|15|20|25|30|35|40|45|50"],
                ["race_frameskip" , "auto" , "disabled|auto|manual"],
                ["race_frameskip_threshold" , "33" , "15|18|21|24|27|30|33|36|39|42|45|48|51|54|57|60"],
                ["race_language" , "english" , "japanese|english"]
            ],


            "Snes9x 2002" : [

                ["snes9x2002_frameskip" , "auto" , "0|auto|auto_threshold|fixed_interval"],
                ["snes9x2002_frameskip_threshold" , "33" , "15|18|21|24|27|30|33|36|39|42|45|48|51|54|57|60"],
                ["snes9x2002_frameskip_interval" , "2" , "0|1|2|3|4|5|6|7|8|9|10"],
                ["snes9x2002_transparency" , "enabled" , "disabled|enabled"],
                ["snes9x2002_low_pass_filter" , "disabled" , "disabled|enabled"],
                ["snes9x2002_low_pass_range" , "60" , "5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95"],
                ["snes9x2002_overclock_cycles" , "disabled" , "disabled|compatible|max"]
            ],

            "Snes9x 2005" : [

                ["snes9x_2005_region" , "auto" , "auto|NTSC|PAL"] ,
                ["snes9x_2005_frameskip" , "auto", "0|auto|manual"] ,
                ["snes9x_2005_frameskip_threshold" , "33" , "15|18|21|24|27|30|33|36|39|42|45|48|51|54|57|60"] ,
                ["snes9x_2005_low_pass_filter" , "disabled", "disabled|enabled"] ,
                ["snes9x_2005_low_pass_range" , "60" , "5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95"] ,
                ["snes9x_2005_overclock_cycles" , "disabled" , "disabled|compatible|max"] ,
                ["snes9x_2005_reduce_sprite_flicker" , "disabled" , "disabled|enabled"]

            ],


            "Stella 2014" : [

                ["stella2014_color_depth" , "16bit" , "16bit|24bit"] ,
                ["stella2014_mix_frames" , "disabled"  , "disabled|mix|ghost_65|ghost_75|ghost_85|ghost_95"] ,
                ["stella2014_low_pass_filter" , "disabled" , "disabled|enabled"] ,
                ["stella2014_low_pass_range" , "60"  , "5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95"] ,
                ["stella2014_paddle_digital_sensitivity" , "50"  , "10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95|100"] ,
                ["stella2014_paddle_analog_sensitivity" , "50" , "10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95|100|105|110|115|120|125|130|135|140|145|150"] ,
                ["stella2014_paddle_analog_response" , "linear" , "linear|quadratic"] ,
                ["stella2014_paddle_analog_deadzone" , "15" , "0|3|6|9|12|15|18|21|24|27|30"] ,
                ["stella2014_stelladaptor_analog_sensitivity" , "20" , "*0-30"] ,
                ["stella2014_stelladaptor_analog_center" , "0" , "-10|-9|-8|-7|-6|-5|-4|-3|-2|-1|0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30"] ,

            ] , 


            "Gearsystem" : [

                ["gearsystem_up_down_allowed" , "Disabled" , "Disabled|Enabled"] ,
                ["gearsystem_system" , "Auto" , "Auto|Master System / Mark III|Game Gear|SG-1000 / Multivision"] ,
                ["gearsystem_region" , "Auto" , "Auto|Master System Japan|Master System Export|Game Gear Japan|Game Gear Export|Game Gear International"] ,
                ["gearsystem_mapper" , "Auto" , "Auto|ROM|SEGA|Codemasters|Korean|SG-1000|MSX|Janggun"] ,
                ["gearsystem_timing" , "Auto" , "Auto|NTSC (60 Hz)|PAL (50 Hz)"] ,
                ["gearsystem_bios_sms" , "Disabled" , "Disabled|Enabled"] ,
                ["gearsystem_bios_gg" , "Disabled" , "Disabled|Enabled"] ,
                ["gearsystem_glasses" , "Both Eyes / OFF" ,"Both Eyes / OFF|Left Eye|Right Eye"]


            ],


            "PicoDrive" : [

                ["picodrive_regio" , "Auto" ,"Auto|Japan NTSC|Japan PAL|US|Europe"] ,
                ["picodrive_smstype" , "Auto" ,"Auto|Game Gear|Master System|SG-1000|SC-3000"] ,
                ["picodrive_smsmapper" , "Auto" ,"Auto|Sega|Codemasters|Korea|Korea MSX|Korea X-in-1|Korea 4-Pak|Korea Janggun|Korea Nemesis|Taiwan 8K RAM"] ,
                ["picodrive_ramcart" , "disabled" ,"disabled|enabled"] ,
                ["picodrive_aspect" , "PAR" ,"PAR|4/3|CRT"] ,
                ["picodrive_ggghost" , "off" ,"off|weak|normal"] ,
                ["picodrive_renderer" , "accurate" , "accurate|good|fast"] ,
                ["picodrive_sound_rate" , "22050" , "16000|22050|32000|44100|native"] ,
                ["picodrive_fm_filter" , "off" , "off|on"] ,
                ["picodrive_smsfm" , "off" , "off|on"] ,
                ["picodrive_dacnoise" , "off" , "off|on"] ,
                ["picodrive_audio_filter" , "disabled" , "disabled|low-pass"] ,
                ["picodrive_lowpass_range" , "60" , "5|10|15|20|25|30|35|40|45|50|55|60|65|70|75|80|85|90|95"] ,
                ["picodrive_input1" , "6 button pad" , "3 button pad|6 button pad|None"] ,
                ["picodrive_input2" , "6 button pad" , "3 button pad|6 button pad|None"] ,
                ["picodrive_drc" , "enabled" , "disabled|enabled"] ,
                ["picodrive_frameskip" , "auto" , "disabled|auto|manual"] ,
                ["picodrive_frameskip_threshold" , "33" , "15|18|21|24|27|30|33|36|39|42|45|48|51|54|57|60"] ,
                ["picodrive_sprlim" , "disabled" ,  "disabled|enabled"] ,
                ["picodrive_overclk68k" , "disabled" , "disabled|+25%|+50%|+75%|+100%|+200%|+400%"]

            ],


            "Gambatte" : [

                ["gambatte_audio_resampler" , "sinc" , "sinc|cc"],
                ["gambatte_dark_filter_level" , "0" , "0|5|10|15|20|25|30|35|40|45|50"],
                ["gambatte_gb_bootloader" , "enabled" , "enabled|disabled" ],
                ["gambatte_gb_colorization" , "internal" , "disabled|auto|GBC|SGB|internal"],
                ["gambatte_gb_hwmode" , "Auto" , "Auto|GB|GBC|GBA"],
                ["gambatte_gb_internal_palette" , "GB - DMG" ,  "GB - DMG|GB - Pocket|GB - Light|GBC - Blue|GBC - Brown|GBC - Dark Blue|GBC - Dark Brown|GBC - Dark Green|GBC - Grayscale|GBC - Green|GBC - Inverted|GBC - Orange|GBC - Pastel Mix|GBC - Red|GBC - Yellow|SGB - 1A|SGB - 1B|SGB - 1C|SGB - 1D|SGB - 1E|SGB - 1F|SGB - 1G|SGB - 1H|SGB - 2A|SGB - 2B|SGB - 2C|SGB - 2D"],
                ["gambatte_gbc_color_correction" , "GBC only" , "GBC only|always|disabled"],
                ["gambatte_gbc_color_correction_mode" , "accurate" , "accurate|fast"] ,
                ["gambatte_gbc_frontlight_position" , "central" , "central|above screen|below screen"],
                ["gambatte_mix_frames" , "disabled" , "disabled|accurate|fast"],
                ["gambatte_turbo_period" , "4" , "*4-120"] ,
                ["gambatte_up_down_allowed" , "disabled" , "disabled|enabled"]


            ]

    } 


        