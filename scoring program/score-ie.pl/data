#!/usr/bin/perl

# USAGE: perl score-ie.pl <output_templates> <answer_templates>

# This program produces two kinds of output:
#
# 1) It will print (to standard output) a table showing the 
#    recall, precision, and f-measure scores for the given 
#    output templates. 
#
# 2) It will automatically generate a file called <output_templates>.trace 
#    (in the working directory) that will show the recall, precision,
#    and f-measure scores for each individual story. The table of scores 
#    for ALL of the stories is also appended to the end of this file. 
#    

# **********************************************************************
#                         DATA STRUCTURES
# **********************************************************************

use Class::Struct; 

struct template => {
  id => '$',
  incident => '$',
  weapons => '$',
  perp_indivs => '$',
  perp_orgs => '$',
  targets => '$',
  victims => '$',
  bogus => '$',
}; 

# **********************************************************************
#                         GLOBAL VARIABLES
# **********************************************************************

$response_file = $ARGV[0];
$answerkey_file = $ARGV[1];

# create trace file with same name as response file + extension .trace
$trace_file = $response_file . ".trace";
open(trace_stream, ">$trace_file") || 
    die "Can't open file: $trace_file\n"; 

my($responses, $answerkeys);  # each is a list of template structures
my($alltemplates_correct) = 0;
my($alltemplates_generated) = 0;
my($alltemplates_true) = 0;
my($alltemplates_incidents_correct) = 0;
my($alltemplates_incidents_generated) = 0;
my($alltemplates_incidents_true) = 0;
my($alltemplates_weapons_correct) = 0;
my($alltemplates_weapons_generated) = 0;
my($alltemplates_weapons_true) = 0;
my($alltemplates_perpindivs_correct) = 0;
my($alltemplates_perpindivs_generated) = 0;
my($alltemplates_perpindivs_true) = 0;
my($alltemplates_perporgs_correct) = 0;
my($alltemplates_perporgs_generated) = 0;
my($alltemplates_perporgs_true) = 0;
my($alltemplates_targets_correct) = 0;
my($alltemplates_targets_generated) = 0;
my($alltemplates_targets_true) = 0;
my($alltemplates_victims_correct) = 0;
my($alltemplates_victims_generated) = 0;
my($alltemplates_victims_true) = 0;


# **********************************************************************
#                         MAIN CODE
# **********************************************************************

$responses = read_templates($response_file);
$answerkeys = read_templates($answerkey_file);
my($num_anskeys) = scalar @$answerkeys;
score_responses($responses, $answerkeys);

# Print score report for stats over ALL templates
#
print trace_stream "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>";
print trace_stream ">>>>>>>>>>>>>>>>>>>>>>>\n\n";
print_score_report("ALL Templates", $alltemplates_incidents_correct,
   $alltemplates_incidents_generated, $num_anskeys,
   $alltemplates_weapons_correct, $alltemplates_weapons_generated,  
   $alltemplates_weapons_true, $alltemplates_perpindivs_correct, 
   $alltemplates_perpindivs_generated, $alltemplates_perpindivs_true,  
   $alltemplates_perporgs_correct, $alltemplates_perporgs_generated, 
   $alltemplates_perporgs_true, $alltemplates_targets_correct, 
   $alltemplates_targets_generated, $alltemplates_targets_true, 
   $alltemplates_victims_correct, $alltemplates_victims_generated, 
   $alltemplates_victims_true, $alltemplates_correct, 
   $alltemplates_generated, $alltemplates_true);

# Display summary score report to standard output
#
display_score_report("ALL Templates", $alltemplates_incidents_correct,
   $alltemplates_incidents_generated, $num_anskeys,
   $alltemplates_weapons_correct, $alltemplates_weapons_generated,  
   $alltemplates_weapons_true, $alltemplates_perpindivs_correct, 
   $alltemplates_perpindivs_generated, $alltemplates_perpindivs_true,  
   $alltemplates_perporgs_correct, $alltemplates_perporgs_generated, 
   $alltemplates_perporgs_true, $alltemplates_targets_correct, 
   $alltemplates_targets_generated, $alltemplates_targets_true, 
   $alltemplates_victims_correct, $alltemplates_victims_generated, 
   $alltemplates_victims_true, $alltemplates_correct, 
   $alltemplates_generated, $alltemplates_true);


# **********************************************************************
#                         SCORING FUNCTIONS
# **********************************************************************

sub score_responses {
    my($responses, $answerkeys) = @_;
    my($i);
    
    $num_responses = @$responses;
    $num_answerkeys = @$answerkeys;
    if (!($num_responses eq $num_answerkeys)) {
	print "**********************************************************\n";
	print "            WARNING!!!! unequal template sets\n";
	print "            $num_responses responses, $num_answerkeys answerkeys\n";
	print "**********************************************************\n";
	for ($i=0; $i < $num_responses; $i++) {
	    $rtemplate = @$responses[$i];
	    $ktemplate = @$answerkeys[$i];
	    my($rid) = "none"; my($kid) = "none";
	    $rid = $rtemplate->id;
	    if ($ktemplate) {
		$kid = $ktemplate->id;
	    }
	    if ($rid !~ /\s*$kid\s*/i) {
		print "MISMATCH: response=$rid  answerkey=$kid\n";
	    }
	}
    }
    else {
	for ($i=0; $i < $num_responses; $i++) {
	    $response = @$responses[$i];
	    $answerkey = @$answerkeys[$i];
	    $response_id = $response->id;
	    $answerkey_id = $answerkey->id;
	    if ($response_id !~ /^$answerkey_id$/i) { # gut check
		print "WARNING: mismatched templates";
		print " ($response_id and $answerkey_id)\n";
	    }
	    else {
		print "Processing text $response_id ...\n";
		print trace_stream "\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>";
		print trace_stream ">>>>>>>>>>>>>>>>>>>>>>>\n\n";
		print trace_stream "      ANSWER KEY \n\n";
		print_template($answerkey);
		print trace_stream "\n      SYSTEM OUTPUT \n\n";
		print_template($response);
		score_template($response, $answerkey);
	    }
	}
    }
}

sub score_template {
    my($response, $key) = @_;
    my($correct_incident, $generated_incident) = 0;
    my($correct_weapons, $generated_weapons, $true_weapons) = 0;
    my($correct_perpindivs, $generated_perpindivs, $true_perpindivs) = 0;
    my($correct_perporgs, $generated_perporgs, $true_perporgs) = 0;
    my($correct_targets, $generated_targets, $true_targets) = 0;
    my($correct_victims, $generated_victims, $true_victims) = 0;
    my($total_correct, $total_generated, $total_true) = 0;

    my(@key_incidents) = ();
    push(@key_incidents, $key->incident);
    if (member($response->incident, \@key_incidents)) {  # member function handles
	$correct_incident++;                             # disjunctions
	$generated_incident++;
	$total_correct++;
	$total_generated++;
    }
    else {
	$correct_incident = 0;
	if ($response->incident !~ /^-$/) {  # make sure slot filled
	    $generated_incident++;
	    $total_generated++;
	}
	else {
	    $generated_incident = 0;
	}
    }
    $total_true = 1;   # for incident slot

    $response_weapons = $response->weapons;
    $key_weapons = $key->weapons;
    $generated_weapons = @$response_weapons;
    $true_weapons = @$key_weapons;
    foreach $weapon (@$response_weapons) {
	if ($found = member($weapon, $key_weapons)) {
	    $correct_weapons++;
	    $key_weapons = remove($found, $key_weapons);
	}
    }

    $response_perpindivs = $response->perp_indivs;
    $key_perpindivs = $key->perp_indivs;
    $generated_perpindivs = @$response_perpindivs;
    $true_perpindivs = @$key_perpindivs;
    foreach $weapon (@$response_perpindivs) {
	if ($found = member($weapon, $key_perpindivs)) {
	    $correct_perpindivs++;
	    $key_perpindivs = remove($found, $key_perpindivs);
	}
    }

    $response_perporgs = $response->perp_orgs;
    $key_perporgs = $key->perp_orgs;
    $generated_perporgs = @$response_perporgs;
    $true_perporgs = @$key_perporgs;
    foreach $weapon (@$response_perporgs) {
	if ($found = member($weapon, $key_perporgs)) {
	    $correct_perporgs++;
	    $key_perporgs = remove($found, $key_perporgs);
	}
    }

    $response_targets = $response->targets;
    $key_targets = $key->targets;
    $generated_targets = @$response_targets;
    $true_targets = @$key_targets;
    foreach $weapon (@$response_targets) {
	if ($found = member($weapon, $key_targets)) {
	    $correct_targets++;
	    $key_targets = remove($found, $key_targets);
	}
    }

    $response_victims = $response->victims;
    $key_victims = $key->victims;
    $generated_victims = @$response_victims;
    $true_victims = @$key_victims;
    foreach $weapon (@$response_victims) {
	if ($found = member($weapon, $key_victims)) {
	    $correct_victims++;
	    $key_victims = remove($found, $key_victims);
	}
    }
    $total_correct = $total_correct + $correct_weapons + 
	$correct_perpindivs + $correct_perporgs + $correct_targets + 
        $correct_victims;  
    $total_generated = $total_generated + $generated_weapons + 
	$generated_perpindivs + $generated_perporgs + 
	$generated_targets + $generated_victims;
    $total_true = $total_true + $true_weapons + $true_perpindivs +
	$true_perporgs + $true_targets + $true_victims;
    
    print_score_report($response->id, $correct_incident, 
       $generated_incident, 1,
       $correct_weapons, $generated_weapons, $true_weapons,
       $correct_perpindivs, $generated_perpindivs, $true_perpindivs, 
       $correct_perporgs, $generated_perporgs, $true_perporgs, 
       $correct_targets, $generated_targets, $true_targets, 
       $correct_victims, $generated_victims, $true_victims,
       $total_correct, $total_generated, $total_true);

    update_global_vars($correct_incident, $generated_incident, 1, 
       $correct_weapons, $generated_weapons, $true_weapons, 
       $correct_perpindivs, $generated_perpindivs, $true_perpindivs, 
       $correct_perporgs, $generated_perporgs, $true_perporgs, 
       $correct_targets, $generated_targets, $true_targets, 
       $correct_victims, $generated_victims, $true_victims, 
       $total_correct, $total_generated, $total_true);
}


# Remove just the *first* occurrence of the item from the list.
# IMPORTANT because some templates (e.g., 0945) contain separate
# entries for the same string (e.g., two distinct occurrences of "PEOPLE").
#
sub remove {
    my($item, $lst) = @_;

    my(@newlst) = ();
    my($found) = 0;
    for ($i=0; $i < @$lst; $i++) {
	if (($found == 0) && (@$lst[$i] eq $item)) {
	    $found = 1;
	}
	else {
	    push(@newlst, @$lst[$i]);
	}
    }
    return(\@newlst);
}


# $answers is a list of possible answers.
# EACH $answer may be a disjunction of options:  option1 / option2 / ...
# If any of the options matches the string, then this is a match
#
sub member {
    my($string, $answers) = @_;

    foreach $answer (@$answers) {
	@options = split /\//, $answer;
	foreach $option (@options) {
	    if (match($option, $string)) {
#		print "Found match: $string $option\n";
		return($answer);  # return ENTIRE answer string
	    }
	}
    }
    return(0);
}

sub match {
    my($str1, $str2) = @_;

    if ($str1 =~ /^\s*\Q$str2\E\s*$/i) {  # allows white space on ends
	return(1);
    }
    else {
	return(0);
    }
}



sub print_score_report {
    my($id, $correct_incident, $generated_incident, $true_incident,
       $correct_weapons, 
       $generated_weapons, $true_weapons, $correct_perpindivs, 
       $generated_perpindivs, $true_perpindivs, $correct_perporgs, 
       $generated_perporgs, $true_perporgs, $correct_targets, 
       $generated_targets, $true_targets, $correct_victims, 
       $generated_victims, $true_victims, $total_correct, 
       $total_generated, $total_true) = @_;

#    print trace_stream "\n********************************************************\n";
    print trace_stream "\n     SCORES for $id\n\n";
#    print trace_stream "********************************************************\n";
    print trace_stream "                RECALL             PRECISION          F-MEASURE\n";
    print_scores("Incident", $correct_incident, $generated_incident, 
		 $true_incident);
    print_scores("Weapons", $correct_weapons, $generated_weapons, 
		 $true_weapons);
    print_scores("Perp_Ind", $correct_perpindivs,
		 $generated_perpindivs, $true_perpindivs);
    print_scores("Perp_Org", $correct_perporgs, $generated_perporgs, 
		 $true_perporgs);
    print_scores("Targets", $correct_targets, $generated_targets, 
		 $true_targets);
    print_scores("Victims", $correct_victims, $generated_victims, 
		 $true_victims);
#    print trace_stream "--------------------------------------------------------\n";
#    print trace_stream "---------------------------------------------------------------\n";
    print trace_stream "--------        --------------     --------------     ----\n";
    print_scores("TOTAL", $total_correct, $total_generated, $total_true);
}


sub display_score_report {
    my($id, $correct_incident, $generated_incident, $true_incident,
       $correct_weapons, 
       $generated_weapons, $true_weapons, $correct_perpindivs, 
       $generated_perpindivs, $true_perpindivs, $correct_perporgs, 
       $generated_perporgs, $true_perporgs, $correct_targets, 
       $generated_targets, $true_targets, $correct_victims, 
       $generated_victims, $true_victims, $total_correct, 
       $total_generated, $total_true) = @_;

#    print "\n********************************************************\n";
    print "\n     Scores for $id\n\n";
#    print "********************************************************\n";
    print "                RECALL             PRECISION          F-MEASURE\n";
    display_scores("Incident", $correct_incident, $generated_incident, 
		 $true_incident);
    display_scores("Weapons", $correct_weapons, $generated_weapons, 
		 $true_weapons);
    display_scores("Perp_Ind", $correct_perpindivs,
		 $generated_perpindivs, $true_perpindivs);
    display_scores("Perp_Org", $correct_perporgs, $generated_perporgs, 
		 $true_perporgs);
    display_scores("Targets", $correct_targets, $generated_targets, 
		 $true_targets);
    display_scores("Victims", $correct_victims, $generated_victims, 
		 $true_victims);
#    print "--------------------------------------------------------\n";
#    print "---------------------------------------------------------------\n";
    print "--------        --------------     --------------     ----\n";
    display_scores("TOTAL", $total_correct, $total_generated, $total_true);
}



# Update global variables
sub update_global_vars {
    my($correct_incident, $generated_incident, $true_incident,
       $correct_weapons, 
       $generated_weapons, $true_weapons, $correct_perpindivs, 
       $generated_perpindivs, $true_perpindivs, $correct_perporgs, 
       $generated_perporgs, $true_perporgs, $correct_targets, 
       $generated_targets, $true_targets, $correct_victims, 
       $generated_victims, $true_victims, $total_correct, 
       $total_generated, $total_true) = @_;

    $alltemplates_correct += $total_correct;
    $alltemplates_generated += $total_generated;
    $alltemplates_true += $total_true;
    $alltemplates_incidents_correct += $correct_incident;
    $alltemplates_incidents_generated += $generated_incident;
    $alltemplates_incidents_true += $true_incident;
    $alltemplates_weapons_correct += $correct_weapons; 
    $alltemplates_weapons_generated += $generated_weapons; 
    $alltemplates_weapons_true += $true_weapons; 
    $alltemplates_perpindivs_correct += $correct_perpindivs; 
    $alltemplates_perpindivs_generated += $generated_perpindivs; 
    $alltemplates_perpindivs_true += $true_perpindivs; 
    $alltemplates_perporgs_correct += $correct_perporgs; 
    $alltemplates_perporgs_generated += $generated_perporgs; 
    $alltemplates_perporgs_true += $true_perporgs; 
    $alltemplates_targets_correct += $correct_targets; 
    $alltemplates_targets_generated += $generated_targets; 
    $alltemplates_targets_true += $true_targets; 
    $alltemplates_victims_correct += $correct_victims; 
    $alltemplates_victims_generated += $generated_victims; 
    $alltemplates_victims_true += $true_victims; 
} 


sub print_scores {
    my($label, $correct, $guessed, $true) = @_;
    my($tally, $padded_tally);

    if ($true == 0) {
	$recall = 0;
    }
    else {
	$recall = $correct / $true;
    }
    if ($guessed == 0) {
	$precision = 0;
    }
    else {
	$precision = $correct / $guessed;
    }
    if (($precision + $recall) == 0) {
	$fmeasure = 0;
    }
    else {
	$fmeasure = (2 * $precision * $recall) / ($precision + $recall);
    }

    $padded_label = pad_w_spaces($label, 15);
    print trace_stream "$padded_label ";
    printf trace_stream "%.2f", $recall;
    print trace_stream " ($correct/$true)\t   ";
    printf trace_stream "%.2f", $precision;
    $tally = sprintf "(%d/%d)", $correct, $guessed;
    $padded_tally = pad_w_spaces($tally, 14);
    print trace_stream " $padded_tally";
    printf trace_stream "%.2f\n", $fmeasure;

}

sub display_scores {
    my($label, $correct, $guessed, $true) = @_;
    my($recall, $precision, $fmeasure, $tally, $padded_tally);

    if ($true eq 0) {
	$recall = 0;
    }
    else {
	$recall = $correct / $true;
    }
    if ($guessed eq 0) {
	$precision = 0;
    }
    else {
	$precision = $correct / $guessed;
    }
    if (($precision + $recall) == 0) {
	$fmeasure = 0;
    }
    else {
	$fmeasure = (2 * $precision * $recall) / ($precision + $recall);
    }
    
    $padded_label = pad_w_spaces($label, 15);
    print "$padded_label ";
    printf "%.2f", $recall;
    print  " ($correct/$true)\t   ";
    printf "%.2f", $precision;
    $tally = sprintf "(%d/%d)", $correct, $guessed;
    $padded_tally = pad_w_spaces($tally, 14);
    print " $padded_tally";
    printf "%.2f\n", $fmeasure;
}

# **********************************************************************
#                         I/O
# **********************************************************************

sub read_templates {
    my($filename) = @_;
    my($line, $id, $incident, $weapon, $perp_indiv, $perp_org);
    my($target, $victim, $last_slot, $template);
    my(@templates) = ();

    my($id) = "";
    $last_slot = "";
    my(@weapons, @perp_indivs, @perp_orgs, @targets, @victims) = ();
    open(stream, $filename) || die "Can't open file: $filename\n";
    while ($line = <stream>) {
	$line =~ s/\n//g;  # strip newline
	if ($line =~ /^\s*$/) {  # if blank line, do nothing
	}
	elsif ($line =~ /^ID:\s+(.*)$/i) {
	    if ($id) {  # save previous template, starting new one
		$template = create_template($id, $incident, \@weapons,
		      \@perp_indivs, \@perp_orgs, \@targets, \@victims);
		push(@templates, $template);
	    }
	    $id = $1;
	    $id =~ s/\s+$//;  # remove trailing white space
	    $last_slot = "id";
	}
	elsif ($line =~ /^INCIDENT:\s+(.*)$/i) {
	    $incident = $1;
	    $incident =~ s/\s+$//;  # remove trailing white space
	    $last_slot = "incident";
	}
	elsif ($line =~ /^WEAPON:\s+(.*)$/i) {
	    $weapon = $1;
	    $weapon =~ s/\s+$//;  # remove trailing white space
	    $last_slot = "weapon";
	    @weapons = ();  
	    if ($weapon !~ /^-$/i) {
		push(@weapons, $weapon);
	    }
	}
	elsif ($line =~ /^PERP INDIV:\s+(.*)$/i) {
	    $perp_indiv = $1;
	    $perp_indiv =~ s/\s+$//;  # remove trailing white space
	    $last_slot = "perp_indiv";
	    @perp_indivs = ();
	    if ($perp_indiv !~ /^-$/i) {
		push(@perp_indivs, $perp_indiv);
	    }
	}
	elsif ($line =~ /^PERP ORG:\s+(.*)$/i) {
	    $perp_org = $1;
	    $perp_org =~ s/\s+$//;  # remove trailing white space
	    $last_slot = "perp_org";
	    @perp_orgs = ();
	    if ($perp_org !~ /^-$/i) {
		push(@perp_orgs, $perp_org);
	    }
	}
	elsif ($line =~ /^TARGET:\s+(.*)$/i) {
	    $target = $1;
	    $target =~ s/\s+$//;  # remove trailing white space
	    $last_slot = "target";
	    @targets = ();
	    if ($target !~ /^-$/i) {
		push(@targets, $target);
	    }
	}
	elsif ($line =~ /^VICTIM:\s+(.*)$/i) {
	    $victim = $1;
	    $victim =~ s/\s+$//;  # remove trailing white space
	    @victims = ();
	    $last_slot = "victim";
	    if ($victim !~ /^-$/i) {
		push(@victims, $victim);
	    }
	}
	elsif ($line =~ /^\s+([\w\d].*)/i) {
	    $item = $1;
	    $item =~ s/\s+$//;  # remove trailing white space
	    if ($last_slot =~ /weapon/i) {
		push(@weapons, $item);
	    }
	    elsif ($last_slot =~ /perp_indiv/i) {
		push(@perp_indivs, $item);
	    }
	    elsif ($last_slot =~ /perp_org/i) {
		push(@perp_orgs, $item);
	    }
	    elsif ($last_slot =~ /target/i) {
		push(@targets, $item);
	    }
	    elsif ($last_slot =~ /victim/i) {
		push(@victims, $item);
	    }
	}
    }
    # don't forget last one!
    $template = create_template($id, $incident, \@weapons,
		\@perp_indivs, \@perp_orgs, \@targets, \@victims);
    push(@templates, $template);
    return(\@templates);
}

sub create_template {
    my($id, $incident, $weapons, $perp_indivs, $perp_orgs, $targets, $victims) = @_;
    my($template);
    
    my(@newweapons) = @$weapons;
    my(@newperp_indivs) = @$perp_indivs;
    my(@newperp_orgs) = @$perp_orgs;
    my(@newtargets) = @$targets;    
    my(@newvictims) = @$victims;  # copy list

    $template = template->new();
    $template->id($id);
    $template->incident($incident);
    $template->weapons(\@newweapons);
    $template->perp_indivs(\@newperp_indivs);
    $template->perp_orgs(\@newperp_orgs);
    $template->targets(\@newtargets);
    $template->victims(\@newvictims);
    return($template);
}

sub print_template {
    my($template) = @_;
    my($label, $id, $incident, $weapons, $perp_indivs, $perp_orgs);
    my($targets, $victims);

    $label = pad_w_spaces("ID:", 15);
    $id = $template->id;
    print trace_stream "$label $id\n";
    $label = pad_w_spaces("INCIDENT:", 15);
    $incident = $template->incident;
    print trace_stream "$label $incident\n";

    $weapons = $template->weapons;	
    $label = pad_w_spaces("WEAPON:", 15);
    if (@$weapons eq 0) {
	print trace_stream "$label -\n";
    }
    else {
	for ($i=0; $i < @$weapons; $i++) {
	    $weapon = @$weapons[$i];
	    print trace_stream "$label $weapon\n";
	    $label = pad_w_spaces("", 15);
	}
    }

    $perp_indivs = $template->perp_indivs;	
    $label = pad_w_spaces("PERP_INDIV:", 15);
    if (@$perp_indivs eq 0) {
	print trace_stream "$label -\n";
    }
    else {
	for ($i=0; $i < @$perp_indivs; $i++) {
	    $perp_indiv = @$perp_indivs[$i];
	    print trace_stream "$label $perp_indiv\n";
	    $label = pad_w_spaces("", 15);
	}
    }

    $perp_orgs = $template->perp_orgs;	
    $label = pad_w_spaces("PERP_ORG:", 15);
    if (@$perp_orgs eq 0) {
	print trace_stream "$label -\n";
    }
    else {
	for ($i=0; $i < @$perp_orgs; $i++) {
	    $perp_org = @$perp_orgs[$i];
	    print trace_stream "$label $perp_org\n";
	    $label = pad_w_spaces("", 15);
	}
    }

    $targets = $template->targets;	
    $label = pad_w_spaces("TARGET:", 15);
    if (@$targets eq 0) {
	print trace_stream "$label -\n";
    }
    else {
	for ($i=0; $i < @$targets; $i++) {
	    $target = @$targets[$i];
	    print trace_stream "$label $target\n";
	    $label = pad_w_spaces("", 15);
	}
    }

    $victims = $template->victims;	
    $label = pad_w_spaces("VICTIM:", 15);
    if (@$victims eq 0) {
	print trace_stream "$label -\n";
    }
    else {
	for ($i=0; $i < @$victims; $i++) {
	    $victim = @$victims[$i];
	    print trace_stream "$label $victim\n";
	    $label = pad_w_spaces("", 15);
	}
    }
}



# Given a string and number N, this function pads spaces onto the right
# side of the string until the string has length N.
#
sub pad_w_spaces {
    my($str,$N) = @_;

    my($len) = length $str;
    while ($len < $N) {
        $str = $str . " ";
        $len = length $str;
    }
    return($str);
}


