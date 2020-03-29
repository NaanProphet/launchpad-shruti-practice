{***********************************************
India Melodic - Slot 1
Author: Native Instruments
Written by: Nikolas Jeroma
Modified: November 26, 2015
*************************************************}

on init
	message("")
	declare $count
	
	set_script_title("India MEL Slot 1")
	declare ui_label $label (2,1)
	set_text($label,"Instrument Prototype:")
	move_control($label,1,1)
	
	set_control_par_str($INST_ICON_ID,$CONTROL_PAR_PICTURE,"india_instrument_icon")
	
	declare ui_menu $instrument_menu
	add_menu_item($instrument_menu,"Bansuri",0)
	add_menu_item($instrument_menu,"Harmonium",1)
	add_menu_item($instrument_menu,"Santur",2)
	add_menu_item($instrument_menu,"Sitar",3)
	add_menu_item($instrument_menu,"Tanpura",4)
	add_menu_item($instrument_menu,"Tumbi",5)
	make_instr_persistent($instrument_menu)
	move_control($instrument_menu,1,2)
	
	pgs_create_key(INSTRUMENT_ID,1)
	pgs_create_key(ACTION_TYPE,1)
	{-1 = prepare, 2 = Mix Preset}
	
	pgs_set_key_val(ACTION_TYPE,0,-1)
	
	read_persistent_var($instrument_menu)
	pgs_set_key_val(ACTION_TYPE,0,0) {0: Inst ID, 1: PerfSld, 2: MixPreset, 3: Tempo, 4: Inst Menu}
	pgs_set_key_val(INSTRUMENT_ID,0,$instrument_menu)
	
	set_key_pressed_support(1)
	
	{bansuri legato variables}
	declare $cur_id
    declare $first_id
    declare $help_id
    declare $help2_id
    declare $press_id
    declare $act_time
    
    declare %note_id[128]
    declare %velo_per_key[128]
    
    declare $max_note
    declare $max_id
    
    declare $last_velocity := 1
	declare $b
	
	declare %key_held[128]
	
	declare %chikari_notes[5] := (37,39,42,44,46)
	
	declare $tumbi_legato_active
	
	declare $tumbi_previous_id
	declare $tumbi_new_id
	
end on

on note

	set_key_pressed($EVENT_NOTE,1)
	
	if ($instrument_menu = 0 and $EVENT_NOTE >= 48)
		{bansuri and tumbi legato}
		ignore_event($EVENT_ID)
	
		if (%note_id[$EVENT_NOTE] # 0)
			exit
		end if
		
		$last_velocity := $EVENT_VELOCITY
		%note_id[$EVENT_NOTE] := $EVENT_ID
		%velo_per_key[$EVENT_NOTE] := $EVENT_VELOCITY
		
		%key_held[$EVENT_NOTE] := 1
		
		if ($act_time # $ENGINE_UPTIME)
		   
			$act_time := $ENGINE_UPTIME
			$help_id := $cur_id
			
			note_off($cur_id)

			$press_id := $EVENT_ID
			$cur_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,0)
			
			$b := 0
			$count := 0
			while($count < 128)
				
				if (%key_held[$count] = 1)
					inc($b)
				end if
				
				inc($count)
			end while
			
			if ($b = 1)
				$first_id := $cur_id
			end if
			
		end if
		
	end if
	
	{TUMBI}
	if ($instrument_menu = 5 and search(%chikari_notes,$EVENT_NOTE) >= 0)
		
		ignore_event($EVENT_ID)
		$tumbi_new_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)			
		
		if ($tumbi_legato_active = 1)
			
			
			note_off($tumbi_previous_id)
			
			{store id}
			$tumbi_previous_id := $tumbi_new_id
			
		else
		
			{first note}
			$tumbi_previous_id := $tumbi_new_id
			$tumbi_legato_active := 1 
			
		end if
	
	end if
	
end on

on release
	
	set_key_pressed($EVENT_NOTE,0)
	
	if ($instrument_menu = 0 and $EVENT_NOTE >= 48)
		
		if ($EVENT_ID = $help_id or $EVENT_ID = $help2_id)
        	exit
   		end if
    
		%note_id[$EVENT_NOTE] := 0
		%key_held[$EVENT_NOTE] := 0
		
		if ($EVENT_ID = $press_id)
			
			$count := 0
			$max_id := 0
			$max_note := 0
			while($count < 128)
				
				if ($max_id < %note_id[$count])
					$max_id := %note_id[$count]
					$press_id := $max_id
					$max_note := $count
				end if
				
				inc($count)
			end while
			
			if ($max_id = 0)
				if (%CC[64] = 0)
					note_off($cur_id)
					note_off($first_id)
				end if
				exit
			end if
			
			if ($act_time # $ENGINE_UPTIME)
				
				$act_time := $ENGINE_UPTIME
				
				note_off($cur_id)
				$cur_id := play_note($max_note,$last_velocity,0,0)              
			   
			end if  
			
		end if
	
	end if
	
	{TUMBI}
	if ($instrument_menu = 5 and search(%chikari_notes,$EVENT_NOTE) >= 0)
		
		if ($EVENT_ID = $tumbi_previous_id)
			$tumbi_legato_active := 0
		end if
	end if
		
end on

on ui_control ($instrument_menu)
	pgs_set_key_val(ACTION_TYPE,0,0) {0: Inst ID, 1: PerfSld, 2: MixPreset, 3: Tempo, 4: Inst Menu}
	pgs_set_key_val(INSTRUMENT_ID,0,$instrument_menu)
end on

on controller

	if ($instrument_menu = 0)
		
		if ($CC_NUM = 64)
			if (%CC[64] = 0)
				$count := 0
				$b := 0
				while($count < 128)
					
					if (%note_id[$count] # 0)
						inc($b)
					end if
					
					inc($count)
				end while
				
				if ($b = 0)
					$help2_id := $cur_id
					note_off($cur_id)           
				end if
				
			end if
		end if
		
		if ($CC_NUM = 123)
			ignore_controller
			note_off(-1)
		end if
    
    end if
end on
