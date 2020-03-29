{***********************************************
India Melodic - Articulation
Author: Native Instruments
Written by: Nikolas Jeroma
Modified: November 18, 2015
*************************************************}

on init

{ function constants }
	
	{GENERAL}
	message("")
	set_script_title("Articulation")
	
	declare const $TUMBI_FIRST_GRP_IDX := 4
	
	declare const $TANPURA_FIRST_GRP_IDX := 0
	
	declare const $MELODY_FIRST_GRP_IDX := 4
	declare const $MELODY_RESO_FIRST_GRP_IDX := 18
	declare const $MELODY_RELEASE_GRP_IDX := 19
	declare const $CHIKARI_FIRST_GRP_IDX := 20
	declare const $CHIKARI_RESO_FIRST_GRP_IDX := 25
	declare const $RESO_STRINGS := 35
	
	declare const $NUM_OF_NOTES_SITAR := 7
	declare const $NUM_OF_NOTES_TANPURA := 4
	
	declare const $TUMBI_1_NOTE := 16
	declare const $TUMBI_2_NOTE := 17
	
	declare const $TANPURA_1_NOTE := 36
	declare const $TANPURA_2_NOTE := 37
	declare const $TANPURA_3_NOTE := 38
	declare const $TANPURA_4_NOTE := 39
	
	{sitar chikari strings}
	declare const $SITAR_1_NOTE := 37 {C#1}
	declare const $SITAR_2_NOTE := 39
	declare const $SITAR_3_NOTE := 42
	declare const $SITAR_4_NOTE := 44
	declare const $SITAR_5_NOTE := 46
	
	{fade times}
	
	declare $TUMBI_FADE_TIME := 140
	declare %SITAR_FADE_TIMES[$NUM_OF_NOTES_SITAR] := (140,140,160,200,400,140,140) {the fade times for the chikari strings in ms}
	
	{first four is male tanpura, second four is female tanpura}
	declare %TANPURA_FADE_TIMES[$NUM_OF_NOTES_TANPURA*2] := (274,302,302,310,274,302,302,310)
	
	declare const $SITAR_ALT_TIME := 1200 {in ms}
	declare const $TUMBI_ALT_TIME := 2000 {in ms}
	
	
	
	
{function } {}

{ function instrument_dentifier }
	
	declare $INSTRUMENT_ID
	make_instr_persistent($INSTRUMENT_ID)
	
	declare const $BANSURI_ID := 0
	declare const $HARMONIUM_ID := 1
	declare const $SANTUR_ID := 2
	declare const $SITAR_ID := 3
	declare const $TANPURA_ID := 4
	declare const $TUMBI_ID := 5
	
	{play and mapping ranges, copied from main script}
	declare $MAPPED_RANGE_MIN := 48 {C2}
	declare $MAPPED_RANGE_MAX := 72 {C6}
	
	make_instr_persistent($MAPPED_RANGE_MIN)
	make_instr_persistent($MAPPED_RANGE_MAX)
	
{function } {}

{ function gui }
	
	declare ui_label $label (2,1)
	set_text($label,"India - Slot 4 (Articulation)")
	
	declare ui_menu $instrument_menu
	add_menu_item($instrument_menu,"Bansuri",0)
	add_menu_item($instrument_menu,"Harmonium",1)
	add_menu_item($instrument_menu,"Santur",2)
	add_menu_item($instrument_menu,"Sitar",3)
	add_menu_item($instrument_menu,"Tanpura",4)
	add_menu_item($instrument_menu,"Tumbi",5)
	make_instr_persistent($instrument_menu)
	
{function } {}

{ function variables }
	
	declare $random_group
	declare $last_random_group := -1
	
	declare $played_note
	declare $played_note_tumbi_rel
	declare $played_velo
	declare $played_grp
	
	declare $played_grp_tumbi_rel
	
	declare $played_grp_2
	declare $played_stroke {0 down, 1 up}
	declare $played_sitar_string
	declare $played_tanpura_string
	
	declare %sitar_ids[$NUM_OF_NOTES_SITAR*2]
	declare %sitar_alternate_last_time[$NUM_OF_NOTES_SITAR]
	declare %sitar_alternate_count[$NUM_OF_NOTES_SITAR]
	
	declare $sitar_release_id
	declare $sitar_release_time_on
	declare $sitar_release_time
	
	declare $tumbi_release_id
	declare $tumbi_release_time_on
	declare $tumbi_release_time
	
	declare polyphonic $release_id
	
	declare $tumbi_note_id
	declare $tumbi_note_id_2
	declare $tumbi_alternate_last_time
	declare $tumbi_alternate_count
	
	declare %tanpura_note_ids[$NUM_OF_NOTES_TANPURA*2]
	declare %fem_tanpura_note_ids[$NUM_OF_NOTES_TANPURA]
	
	declare polyphonic $original_vol {received volume}
	declare polyphonic $original_tune {received tune}
	declare polyphonic $original_group {received tune}
	
	{legato mode}
	declare $bansuri_legato_active {1 if the next note is a legato note}
	
	declare $bansuri_previous_id
	declare $bansuri_new_id
	
	declare $bansuri_note_counter
	
	declare $santur_key_switch
	
	declare const $SEQ_SCRIPT_SLOT := 1
	
	declare polyphonic $played_id
	
	declare polyphonic $played_id_2
	
	declare polyphonic $played_vol
	declare polyphonic $played_wait
	declare polyphonic $played_duration
	
	declare polyphonic $new_id
	
	declare $played_string
	
	declare $run_flag_sequencer
	
	declare %key_id[128]
	
	declare %key_down_bansuri[128]
	
{function } {}



end on

{ function instrument_menu }

on ui_control ($instrument_menu)
	
	$INSTRUMENT_ID := $instrument_menu
	
	select ($INSTRUMENT_ID)
		
		case $BANSURI_ID

			$MAPPED_RANGE_MIN := 56 {Ab2}
			$MAPPED_RANGE_MAX := 91 {G5}
			
		case $HARMONIUM_ID
			
			$MAPPED_RANGE_MIN := 48 {C2}
			$MAPPED_RANGE_MAX := 86 {D5}
			
		case $SANTUR_ID
		
			$MAPPED_RANGE_MIN := 48 {C2}
			$MAPPED_RANGE_MAX := 79 {G4}
			
		case $SITAR_ID
		
			$MAPPED_RANGE_MIN := 48 {C2}
			$MAPPED_RANGE_MAX := 79 {G4}
			
		case $TANPURA_ID

			$MAPPED_RANGE_MIN := 48 {C2}
			$MAPPED_RANGE_MAX := 84 {C5}
			
		case $TUMBI_ID

			$MAPPED_RANGE_MIN := 63 {Eb3}
			$MAPPED_RANGE_MAX := 80 {Ab4}
				
	end select
	
end on
	
{function } {}	

on note
	
	$original_vol := get_event_par($EVENT_ID,$EVENT_PAR_VOLUME)
	$original_tune := get_event_par($EVENT_ID,$EVENT_PAR_TUNE)
	$original_group := get_event_par($EVENT_ID,$EVENT_PAR_1)
		
	
	if (get_event_par($EVENT_ID,$EVENT_PAR_SOURCE) = $SEQ_SCRIPT_SLOT and get_event_par($EVENT_ID,$EVENT_PAR_2) >= 2)
		
		ignore_event($EVENT_ID)
		disallow_group($ALL_GROUPS)
		
		select ($INSTRUMENT_ID)

			{ function bansuri }	
				case $BANSURI_ID
					
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2 and in_range($EVENT_NOTE,$MAPPED_RANGE_MIN,$MAPPED_RANGE_MAX))
						
						
						inc($bansuri_note_counter)
						
						{first note}
						if ($bansuri_note_counter = 1 and $bansuri_legato_active = 0)
							
							$bansuri_new_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
							set_event_par_arr($bansuri_new_id,$EVENT_PAR_ALLOW_GROUP,1,4)
							set_event_par($bansuri_new_id,$EVENT_PAR_2,2)
							change_tune($bansuri_new_id,$original_tune,0)
							
							$bansuri_previous_id := $bansuri_new_id
							$bansuri_legato_active := 1 
							exit
							
						end if
						
						
						{legato played note}
						if ($bansuri_legato_active = 1)
						
							{kill previous note}
							fade_out($bansuri_previous_id,60 * 1000,1)
							$bansuri_new_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
							fade_in($bansuri_new_id,40 * 1000)
							set_event_par_arr($bansuri_new_id,$EVENT_PAR_ALLOW_GROUP,1,5)
							set_event_par($bansuri_new_id,$EVENT_PAR_2,2)
							change_tune($bansuri_new_id,$original_tune,0)
							
							{store id}
							$bansuri_previous_id := $bansuri_new_id
					
						end if
						
						
					end if
					
			{function } {}
			
			{ function harmonium }
			
				case $HARMONIUM_ID

					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2)
					
						{main notes}
						$played_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,4)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,5)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,6)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,7)
						set_event_par($played_id,$EVENT_PAR_2,2)
						change_tune($played_id,$original_tune,0)
						
						{key clicks}
						$played_id_2 := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
						set_event_par_arr($played_id_2,$EVENT_PAR_ALLOW_GROUP,1,8)
						
					end if
						
						
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 3)
						
						{drone root}
						
						$played_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,11)
						
						change_tune($played_id,$original_tune,0)
					
					end if
					
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 4)
						
						{drone 5th or 4th}
						
						$played_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,12)
						
						change_tune($played_id,$original_tune,0)
					
					end if
					
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 5)
						
						{bellow noise}
						
						$played_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,0)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,10)
						
					end if
					
			{function } {}
					
			{ function santur }
			
				case $SANTUR_ID
						
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 3 and $EVENT_NOTE = 37)
						$santur_key_switch := 1
					end if
					
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 3 and $EVENT_NOTE = 39)
						fade_out(by_marks($MARK_2),((($EVENT_VELOCITY - 1) * (20 - 500) / (127 - 1)) + 500) * 1000,1)
					end if
					
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2)
						
						{fade out sounding note}
						if (event_status(%key_id[$EVENT_NOTE])= $EVENT_STATUS_NOTE_QUEUE)
      						 fade_out(%key_id[$EVENT_NOTE],10000,1)
  						 end if
						
						{main notes}
						$played_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,4+$santur_key_switch)
						set_event_mark($played_id,$MARK_2)
						change_tune($played_id,$original_tune,0)
						
						%key_id[$EVENT_NOTE] := $played_id
						
					end if
					
					{drone notes, no key switch here}
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 4)
						
						{fade out sounding note}
						if (event_status(%key_id[$EVENT_NOTE])= $EVENT_STATUS_NOTE_QUEUE)
      						 fade_out(%key_id[$EVENT_NOTE],10000,1)
  						 end if
						
						{main notes}
						$played_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,4)
						set_event_mark($played_id,$MARK_2)
						change_tune($played_id,$original_tune,0)
						
						%key_id[$EVENT_NOTE] := $played_id
						
					end if
					
					
					
					
			{function } {}
			
			{ function sitar }
			
				case $SITAR_ID
				
				{RESONANCE STRINGS}
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 4)
					
					$played_grp := $RESO_STRINGS
					$played_note := $EVENT_NOTE
					
					$new_id := play_note($played_note,$EVENT_VELOCITY,0,-1)
					set_event_par_arr($new_id,$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
					set_event_par($new_id,$EVENT_PAR_2,4)
					change_tune($new_id,$original_tune,0)
					
				end if
				
				{CHIKARI STRING}
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 3)
					
					{get correct string}
					select($EVENT_NOTE)
						case $SITAR_1_NOTE
							$played_sitar_string := 0
						case $SITAR_2_NOTE
							$played_sitar_string := 1
						case $SITAR_3_NOTE
							$played_sitar_string := 2
						case $SITAR_4_NOTE
							$played_sitar_string := 3
						case $SITAR_5_NOTE
							$played_sitar_string := 4
					end select
					
					{get stroke, up or down}
					if ($ENGINE_UPTIME - %sitar_alternate_last_time[$played_sitar_string] < $SITAR_ALT_TIME and %sitar_alternate_last_time[$played_sitar_string] # 0)
						
						{speed alternation active}
						if (%sitar_alternate_count[$played_sitar_string] = 0)
							$played_stroke := 0
							%sitar_alternate_count[$played_sitar_string] := 1
						else
							$played_stroke := 1
							%sitar_alternate_count[$played_sitar_string] := 0
						end if
					else
						{speed alternation inactive - play downstroke}
						
						$played_stroke := 0
						%sitar_alternate_count[$played_sitar_string] := 0
					end if
					
					%sitar_alternate_last_time[$played_sitar_string] := $ENGINE_UPTIME
					
					{chikari strings}
					$played_grp := $CHIKARI_FIRST_GRP_IDX + $played_sitar_string
					$played_note := 36 + $played_sitar_string + ($played_stroke * 12)
					
					{fade in last sounding note}
					if (event_status(%sitar_ids[$played_sitar_string])= $EVENT_STATUS_NOTE_QUEUE)
						fade_out(%sitar_ids[$played_sitar_string],%SITAR_FADE_TIMES[$played_sitar_string]*1000,1)
					end if
					
					{trigger note}
					%sitar_ids[$played_sitar_string] := play_note($played_note,$EVENT_VELOCITY,0,-1)
					set_event_par_arr(%sitar_ids[$played_sitar_string],$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
					change_tune(%sitar_ids[$played_sitar_string],$original_tune,0)
					
					{RESONANCE}
					$played_grp := $CHIKARI_RESO_FIRST_GRP_IDX + $played_sitar_string
					$played_note := 36 + $played_sitar_string
					
					{fade in last sounding note}
					if (event_status(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string])= $EVENT_STATUS_NOTE_QUEUE)
						fade_out(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],%SITAR_FADE_TIMES[$played_sitar_string]*1000,1)
					end if
					
					{trigger note}
					%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string] := play_note($played_note,$EVENT_VELOCITY,0,-1)
					set_event_par_arr(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
					set_event_par_arr(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],$EVENT_PAR_ALLOW_GROUP,1,$played_grp+5)
					change_tune(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],$original_tune,0)		
					
							
				end if
					
				{MELODY STRING}
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2)
					
					$played_sitar_string := 5
					
					{get stroke, up or down}
					if ($ENGINE_UPTIME - %sitar_alternate_last_time[$played_sitar_string] < $SITAR_ALT_TIME and %sitar_alternate_last_time[$played_sitar_string] # 0)
						
						{speed alternation active}
						if (%sitar_alternate_count[$played_sitar_string] = 0)
							$played_stroke := 0
							%sitar_alternate_count[$played_sitar_string] := 1
						else
							$played_stroke := 1
							%sitar_alternate_count[$played_sitar_string] := 0
						end if
					else
						{speed alternation inactive - play downstroke}
						$played_stroke := 0
						%sitar_alternate_count[$played_sitar_string] := 0
					end if
					
					%sitar_alternate_last_time[$played_sitar_string] := $ENGINE_UPTIME
					
					{get group}
					$played_grp := $MELODY_FIRST_GRP_IDX + ($played_stroke*2) + random(0,1)
					
					$played_note := $EVENT_NOTE
					
					$sitar_release_time_on := $ENGINE_UPTIME
					
					{fade in last sounding note}
					if (event_status(%sitar_ids[$played_sitar_string])= $EVENT_STATUS_NOTE_QUEUE)
						
						fade_out(%sitar_ids[$played_sitar_string],%SITAR_FADE_TIMES[$played_sitar_string]*1000,1)
					end if
					
					{trigger note}
					%sitar_ids[$played_sitar_string] := play_note($played_note,$EVENT_VELOCITY,0,-1)
					set_event_par_arr(%sitar_ids[$played_sitar_string],$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
					change_tune(%sitar_ids[$played_sitar_string],$original_tune,0)
					set_event_par(%sitar_ids[$played_sitar_string],$EVENT_PAR_2,3)
					
					{RESONANCE}
					$played_grp := $MELODY_RESO_FIRST_GRP_IDX 
					$played_note := $EVENT_NOTE
					
					{fade in last sounding note}
					{if (event_status(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string])= $EVENT_STATUS_NOTE_QUEUE)
						fade_out(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],%SITAR_FADE_TIMES[$played_sitar_string]*1000,1)
					end if}
					
					{trigger note}
					%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string] := play_note($played_note,$EVENT_VELOCITY,0,-1)
					set_event_par_arr(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
					change_tune(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],$original_tune,0)
					
					
				end if
				
				{SITAR SLIDES}
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 5)
					
					$played_sitar_string := 5
					%sitar_alternate_last_time[$played_sitar_string] := $ENGINE_UPTIME
					
					{get group}
					$played_grp := $original_group
					
					$played_note := $EVENT_NOTE
					
					$sitar_release_time_on := $ENGINE_UPTIME
					
					{fade in last sounding note}
					if (event_status(%sitar_ids[$played_sitar_string])= $EVENT_STATUS_NOTE_QUEUE)
						fade_out(%sitar_ids[$played_sitar_string],%SITAR_FADE_TIMES[$played_sitar_string]*1000,1)
					end if
					
					{trigger note}
					%sitar_ids[$played_sitar_string] := play_note($played_note,$EVENT_VELOCITY,0,-1)
					set_event_par_arr(%sitar_ids[$played_sitar_string],$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
					change_tune(%sitar_ids[$played_sitar_string],$original_tune,0)
					change_vol(%sitar_ids[$played_sitar_string],$original_vol,0)
					set_event_par(%sitar_ids[$played_sitar_string],$EVENT_PAR_2,3)
					
					{RESONANCE}
					$played_grp := $MELODY_RESO_FIRST_GRP_IDX 
					$played_note := $EVENT_NOTE + get_event_par($EVENT_ID,$EVENT_PAR_3)
					
					{fade in last sounding note}
					{if (event_status(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string])= $EVENT_STATUS_NOTE_QUEUE)
						fade_out(%sitar_ids[$NUM_OF_NOTES_SITAR + $played_sitar_string],%SITAR_FADE_TIMES[$played_sitar_string]*1000,1)
					end if}
					
					{trigger note}
					$played_id := play_note($played_note,$EVENT_VELOCITY,0,-1)
					set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
					change_vol($played_id,$original_vol-8000,0)
					change_tune($played_id,$original_tune,0)
					
				end if
					
			{function } {}
				
			{ function tanpura }
			
				case $TANPURA_ID
					
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 4 and $EVENT_NOTE = 37)
						fade_out(by_marks($MARK_3),((($EVENT_VELOCITY - 1) * (20 - 1000) / (127 - 1)) + 1000) * 1000,1)
					end if
					
					if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2 and in_range($EVENT_NOTE,$MAPPED_RANGE_MIN,$MAPPED_RANGE_MAX))
						
						{fade out sounding note}
						if (event_status(%key_id[$EVENT_NOTE])= $EVENT_STATUS_NOTE_QUEUE)
      						 fade_out(%key_id[$EVENT_NOTE],200 * 1000,1)
  						 end if
						
						{main notes}
						$played_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,-1)
						set_event_par_arr($played_id,$EVENT_PAR_ALLOW_GROUP,1,9)
						change_tune($played_id,$original_tune,0)
						set_event_mark($played_id,$MARK_3)
						
						%key_id[$EVENT_NOTE] := $played_id
						
					end if
					
					
			{function } {}
			
			{ function tumbi }
		
			case $TUMBI_ID
			
			if (in_range($EVENT_NOTE,$MAPPED_RANGE_MIN,$MAPPED_RANGE_MAX))
				
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2)
				
				{get stroke, up or down}
					if ($ENGINE_UPTIME - $tumbi_alternate_last_time < $TUMBI_ALT_TIME and $tumbi_alternate_last_time # 0)
						
						{speed alternation active}
						if ($tumbi_alternate_count = 0)
							$played_stroke := 0
							$tumbi_alternate_count := 1
						else
							$played_stroke := 1
							$tumbi_alternate_count := 0
						end if
					else
						{speed alternation inactive - play downstroke}
						
						$played_stroke := 0
						$tumbi_alternate_count := 0
					end if
					
					$tumbi_alternate_last_time := $ENGINE_UPTIME
					
				end if
				
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 3)
					$played_stroke := get_event_par($EVENT_ID,$EVENT_PAR_1)
				end if
				
				{get group}
				$played_grp := $TUMBI_FIRST_GRP_IDX + ($played_stroke * 3) + random(0,2)
				
				$played_grp_2 := $TUMBI_FIRST_GRP_IDX + ($played_stroke * 3) + random(0,2) + 6
				
				{get note}
				$played_note := $EVENT_NOTE
				
				{fade in last sounding note}
				{if (event_status($tumbi_note_id_2)= $EVENT_STATUS_NOTE_QUEUE)
					fade_out($tumbi_note_id_2,$TUMBI_FADE_TIME*1000,1)
				end if
				}
				
				$tumbi_release_time_on := $ENGINE_UPTIME
				
				{trigger noise}
				$tumbi_note_id := play_note($played_note,$EVENT_VELOCITY,0,-1)
				set_event_par_arr($tumbi_note_id,$EVENT_PAR_ALLOW_GROUP,1,$played_grp_2)
				set_event_par($tumbi_note_id,$EVENT_PAR_2,4)
				
				wait(20*1000)
				
				{trigger note}
				$tumbi_note_id_2 := play_note($played_note,$EVENT_VELOCITY,0,-1)
				set_event_par_arr($tumbi_note_id_2,$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
				change_tune($tumbi_note_id_2,$original_tune,0)
			end if
			
		
		{function } {}
	
		end select
	
	end if
	
	if (get_event_par($EVENT_ID,$EVENT_PAR_SOURCE) = $SEQ_SCRIPT_SLOT and get_event_par($EVENT_ID,$EVENT_PAR_2) = 1)

		{ function tanpura_machine }
		
		ignore_event($EVENT_ID)
		disallow_group($ALL_GROUPS)
		
		{seq start and stop}
		if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 1 and in_range($EVENT_NOTE,0,1))
			$run_flag_sequencer := $EVENT_NOTE
			if ($run_flag_sequencer = 0)
				fade_out(by_marks($MARK_1),300000,1)
			end if
			exit
		end if
		
		$played_wait := get_event_par($EVENT_ID,$EVENT_PAR_0)
		$played_grp := get_event_par($EVENT_ID,$EVENT_PAR_1)
		$played_vol := get_event_par($EVENT_ID,$EVENT_PAR_VOLUME)
		$played_note := $EVENT_NOTE + (random(0,1) * 12)
		$played_string := $played_grp
		$played_duration := get_event_par($EVENT_ID,$EVENT_PAR_3)
		
		$played_velo := 1 + (random(0,2) * 45)
		
		
		if ($played_wait > 0)
			wait($played_wait)
		end if
		
		if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 1 and $run_flag_sequencer = 1)
			
			{fade out last sounding note}
			if (event_status(%tanpura_note_ids[$played_string])= $EVENT_STATUS_NOTE_QUEUE)
				fade_out(%tanpura_note_ids[$played_string],%TANPURA_FADE_TIMES[$played_string]*1000,1)
			end if
			
			%tanpura_note_ids[$played_string] := play_note($played_note,$played_velo,0,$played_duration)
			set_event_par_arr(%tanpura_note_ids[$played_string],$EVENT_PAR_ALLOW_GROUP,1, $played_grp)
			set_event_mark(%tanpura_note_ids[$played_string],$MARK_1)
			
		end if
			
	

{function } {}

	end if
	
	if (get_event_par($EVENT_ID,$EVENT_PAR_SOURCE) = $SEQ_SCRIPT_SLOT and get_event_par($EVENT_ID,$EVENT_PAR_2) = 3 and $INSTRUMENT_ID = $TANPURA_ID)

		{ function tanpura machine notes }
		
		ignore_event($EVENT_ID)
		disallow_group($ALL_GROUPS)
		
		$played_grp := get_event_par($EVENT_ID,$EVENT_PAR_1)
		$played_vol := get_event_par($EVENT_ID,$EVENT_PAR_VOLUME)
		$played_note := $EVENT_NOTE + (random(0,1) * 12)
		$played_string := $played_grp
		$played_duration := get_event_par($EVENT_ID,$EVENT_PAR_3)
		
		%tanpura_note_ids[$played_string] := play_note($played_note,$EVENT_VELOCITY,0,$played_duration)
		set_event_par_arr(%tanpura_note_ids[$played_string],$EVENT_PAR_ALLOW_GROUP,1, $played_grp)
		set_event_mark(%tanpura_note_ids[$played_string],$MARK_1)
		set_event_mark(%tanpura_note_ids[$played_string],$MARK_3)

{function } {}

	end if
	
end on

{ function release }

on release
	
	{santur}
	if ($INSTRUMENT_ID = $SANTUR_ID and $EVENT_NOTE = 37 and get_event_par($EVENT_ID,$EVENT_PAR_SOURCE) = $SEQ_SCRIPT_SLOT)

		$santur_key_switch := 0
		
	end if
	
	{bansuri}
	if ($INSTRUMENT_ID = $BANSURI_ID and in_range($EVENT_NOTE,$MAPPED_RANGE_MIN,$MAPPED_RANGE_MAX) and get_event_par($EVENT_ID,$EVENT_PAR_SOURCE) = $SEQ_SCRIPT_SLOT)
		
		dec($bansuri_note_counter)
		
		if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2)
			
			if ($EVENT_ID = $bansuri_previous_id and %CC[64] < 64)
				$bansuri_legato_active := 0
			end if
			
			{last note released}
			if ($bansuri_note_counter = 0)
				
				if (%CC[64] < 64)
					$bansuri_legato_active := 0
				else
					set_event_mark($EVENT_ID,$MARK_4)
					ignore_event($EVENT_ID)
				end if
				
			end if
			
			{legato note with fade out released}
			if ($bansuri_legato_active = 1)
				ignore_event($EVENT_ID)
			end if
				
		end if
			
	end if
	
	{harmonium}
	if ($INSTRUMENT_ID = $HARMONIUM_ID and in_range($EVENT_NOTE,$MAPPED_RANGE_MIN,$MAPPED_RANGE_MAX))
		
		if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 2)
		
			disallow_group($ALL_GROUPS)
			$release_id := play_note($EVENT_NOTE,$EVENT_VELOCITY,0,0)
			set_event_par_arr($release_id,$EVENT_PAR_ALLOW_GROUP,1,9)
			
			{sustain pedal}
			set_event_mark($EVENT_ID, $MARK_4)
			if(%CC[64] >= 64)
				ignore_event($EVENT_ID)
			end if
			
		end if
		
	end if
	
	{sitar}
	if ($INSTRUMENT_ID = $SITAR_ID)
		
		if (get_event_par($EVENT_ID,$EVENT_PAR_2) # 4)
	
			if (in_range($EVENT_NOTE,$MAPPED_RANGE_MIN,$MAPPED_RANGE_MAX))
				
				disallow_group($ALL_GROUPS)
				
				$played_grp := $MELODY_RELEASE_GRP_IDX
				$played_note := $EVENT_NOTE
			
				$sitar_release_id := play_note($played_note,100,0,0)
				set_event_par_arr($sitar_release_id,$EVENT_PAR_ALLOW_GROUP,1,$played_grp)
				
				$sitar_release_time := $ENGINE_UPTIME - $sitar_release_time_on
				
				change_vol($sitar_release_id,$sitar_release_time * -30,0)
				
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) = 3)
					
					{sustain pedal}
					set_event_mark($EVENT_ID, $MARK_4)
					if(%CC[64] >= 64)
						ignore_event($EVENT_ID)
					end if
				
				end if
				
			end if
		
		end if
	
	end if
	
	{tumbi}
	if ($INSTRUMENT_ID = $TUMBI_ID)

			if (get_event_par($EVENT_ID,$EVENT_PAR_SOURCE) = $CURRENT_SCRIPT_SLOT)
			
				if (get_event_par($EVENT_ID,$EVENT_PAR_2) # 4)
				
					if (in_range($EVENT_NOTE,$MAPPED_RANGE_MIN,$MAPPED_RANGE_MAX))
						
						disallow_group($ALL_GROUPS)
						
						$played_grp_tumbi_rel := 16 + random(0,2)
						$played_note_tumbi_rel := $EVENT_NOTE
					
						$tumbi_release_id := play_note($played_note_tumbi_rel,100,0,0)
						set_event_par_arr($tumbi_release_id,$EVENT_PAR_ALLOW_GROUP,1,$played_grp_tumbi_rel)
						
						$tumbi_release_time := $ENGINE_UPTIME - $tumbi_release_time_on
						
						change_vol($tumbi_release_id,$tumbi_release_time * -30,0)
						
						{sustain pedal}
						set_event_mark($EVENT_ID, $MARK_4)
						if(%CC[64] >= 64)
							ignore_event($EVENT_ID)
						end if
						
					end if
				
				end if
			
			end if
		
	
	end if

end on

{function } {}

{ function controller }

on controller
	if ($INSTRUMENT_ID = $BANSURI_ID)
		if (%CC_TOUCHED[64] > 0 and %CC[64] < 64)
			note_off(by_marks($MARK_4))
		end if
	end if
	
	if ($INSTRUMENT_ID = $HARMONIUM_ID)
		if(%CC_TOUCHED[64] > 0 and %CC[64] < 64)
			note_off(by_marks($MARK_4))
		end if
	end if
	
	if ($INSTRUMENT_ID = $SITAR_ID)
		if(%CC_TOUCHED[64] > 0 and %CC[64] < 64)
			note_off(by_marks($MARK_4))
		end if
	end if
	
	if ($INSTRUMENT_ID = $TUMBI_ID)
		if (%CC_TOUCHED[64] > 0 and %CC[64] < 64)
			note_off(by_marks($MARK_4))
		end if
	end if
	
end on

{function } {}

on persistence_changed
	
	$bansuri_note_counter := 0
	$bansuri_legato_active := 0

end on

{END OF SCRIPT}
