<?php
/**
 * Fetches and displays the form.
 */
function ddcl_bb_splice_cover_plate_bolted_form_page()
{
	global $user;
	$data = '';
	if (!$user)
	{
		$data .= "Please login to give feedback";
	} //!$user
	/************* check if user has already submitted a proposal **************/
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step1_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step1_feedback');
	$query->condition('uid', $user->uid);
	$query->orderBy('id', 'DESC');
	$query->range(0, 1);
	$feedback_q = $query->execute();
	if ($feedback_q)
	{
		if ($feedback_data = $feedback_q->fetchObject())
		{
			if ($feedback_data->submitted == 1)
			{
				$data = drupal_set_message(t('You have already submitted the feedback.'), 'status');
				$data .= drupal_goto('');
				return $data;
			} //$feedback_data->submitted == 1
			else
			{
				$ddcl_bb_splice_cover_plate_bolted_step1_form = drupal_get_form("ddcl_bb_splice_cover_plate_bolted_step1_form");
				$data .= drupal_render($ddcl_bb_splice_cover_plate_bolted_step1_form);
			}
		} //$feedback_data = $feedback_q->fetchObject()
		else
		{
			$ddcl_bb_splice_cover_plate_bolted_step1_form = drupal_get_form("ddcl_bb_splice_cover_plate_bolted_step1_form");
			$data .= drupal_render($ddcl_bb_splice_cover_plate_bolted_step1_form);
		}
	} //$feedback_q
	//$data .= drupal_get_form('ddcl_bb_splice_cover_plate_bolted_step1_form');
	return $data;
}
function ddcl_bb_splice_cover_plate_bolted_step1_form($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	global $base_url;
	$markup_text = "Form Title";
	// All the real form fields.
	$form = array();
	$form['step1_header'] = array(
		'#markup' => $markup_text,
		'#required' => true
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step1_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step1_feedback');
	$query->condition('uid', $user->uid);
	$form_step1_data = $query->execute();
	if ($form_step1_data)
	{
		if ($step1_data = $form_step1_data->fetchObject())
		{
			/* everything ok */
		} //$step1_data = $form_step1_data->fetchObject()
		/*else
		{
		drupal_set_message(t('Invalid form selected. Please try again.'), 'error');
		//drupal_goto('lab_migration/manage_proposal');
		return;
		}*/
	} //$form_step1_data
	$form['step1_field1_name'] = array(
		'#title' => 'Name',
		'#type' => 'textfield',
		'#default_value' => $step1_data->name,
		'#required' => TRUE
	);
	$form['step1_field2_email_id'] = array(
		'#type' => 'textfield',
		'#title' => t('Email'),
		'#size' => 30,
		'#value' => $user->mail,
		'#disabled' => TRUE,
		'#required' => TRUE
		//'#default_value' => $form_state['storage']['values'][1]['step1_field2_email_id']
	);
	$form['step1_field3_institute'] = array(
		'#title' => 'Institute / Company',
		'#type' => 'textfield',
		'#default_value' => $step1_data->institute,
		'#required' => TRUE
	);
	$form['step1_field4_current_position'] = array(
		'#title' => 'Current position',
		'#type' => 'textfield',
		'#default_value' => $step1_data->current_position,
		'#required' => TRUE
	);
	$form["step1_page_id"] = array(
		"#type" => "hidden",
		"#value" => "step1"
	);
	$form['next1'] = array(
		'#type' => 'submit',
		'#value' => 'Save & Next',
		'#submit' => array(
			'ddcl_bb_splice_cover_plate_bolted_step1_form_submit'
		)
	);
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step1_form_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step1_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step1_feedback');
	$query->condition('uid', $user->uid);
	$form_step1_data = $query->execute();
	if ($form_step1_data)
	{
		if ($step1_data = $form_step1_data->fetchObject())
		{
			$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET name=:name, email_id=:email_id, institute=:institute, current_position=:current_position WHERE uid=:uid ";
			$args = array(
				":uid" => $user->uid,
				":name" => _field_sentence_case($v['step1_field1_name']),
				":email_id" => $v['step1_field2_email_id'],
				":institute" => _field_sentence_case($v['step1_field3_institute']),
				":current_position" => _field_sentence_case($v['step1_field4_current_position'])
			);
			db_query($query, $args);
		} //$step1_data = $form_step1_data->fetchObject()
		else
		{
			$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step1_feedback} (uid, name, email_id, institute, current_position, data_reletion, inserted_on) VALUES (:uid,:name,:email_id, :institute, :current_position, :data_reletion,:inserted_on)";
			$args = array(
				":uid" => $user->uid,
				":name" => $v['step1_field1_name'],
				":email_id" => $v['step1_field2_email_id'],
				":institute" => $v['step1_field3_institute'],
				":current_position" => $v['step1_field4_current_position'],
				":data_reletion" => "step1",
				":inserted_on" => date('Y-m-d')
			);
			db_query($query, $args);
		}
	} //$form_step1_data
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step2/' . $user->uid;
}
/*************************************************************************/
/************************ Step 2 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step2_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('a. Material strength > i. Yield stress limit > ii. Ultimate strength limit'));
	$img_path = $base_url . '/' . drupal_get_path("module", "osdag_response_form") . '/images';
	$markup_text = '
	<b><strong> a. Material Strength </strong></b><br>
		&emsp; <b><strong> i. Yield stress limits </strong></b>[Reference: Clause 2.2.4.2, Table 1, IS 800 : 2007] <br>					
					<center>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
					  <mn>165</mn>
					  <mo>&lt;</mo>
					  <msub>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mi>f</mi>
					    </mrow>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>y</mtext>
					    </mrow>
					  </msub>
					  <mo>&lt;</mo>
					  <mn>450</mn>
					</math>
					</center>		
		<br>
		&emsp; <b><strong> ii. Ultimate strength limits </strong></b> [Reference: Clause 2.2.4.2, Table 1, IS 800 : 2007] <br>
					<center>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
					  <mn>290</mn>
					  <mo>&lt;</mo>
					  <msub>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mi>f</mi>
					    </mrow>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>u</mtext>
					    </mrow>
					  </msub>
					  <mo>&lt;</mo>
					  <mn>590</mn>
					</math>
					</center>	
					
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>u</mtext>
						  </msub>
						</math> = Characteristic ultimate tensile stress <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;	
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<strong> Note :</strong> All units in MPa
				<hr>
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;				
				<img src="' . $img_path . '/Table1IS800.jpg" width="80%" height="80%" align="middle" />
				<br><br>
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
				Figure: Table 1, IS 800 : 2007	
			<hr>';
	$form = array();
	$form['step2_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step2-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step2_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step2_feedback');
	$query->condition('uid', $user->uid);
	$form_step2_data = $query->execute();
	if ($form_step2_data)
	{
		if ($step2_data = $form_step2_data->fetchObject())
		{
			$form['step2_field1_fieldset']['step2_field1_question1'] = array(
				'#markup' => $markup_text,
				'#required' => true
			);
			$form['step2_field1_fieldset']['step2_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step2_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step2_field1_fieldset']['step2_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step2_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step2_field1_fieldset\\[step2_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step2_data->id, $step2_data->data_relation);
			$icom = 1;
			$form['step2_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr><strong>Earlier comments:</strong><hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step2_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step2_num_comment']))
			{
				$form_state['step2_num_comment'] = 1;
			} //empty($form_state['step2_num_comment'])
			$step2_temp1 = 0;
			for ($step2_i = 0; $step2_i < $form_state['step2_num_comment']; $step2_i++)
			{
				$step2_temp1 = $step2_i;
				$form['step2_field1_fieldset'][$step2_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step2_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step2_field1_fieldset']["step2_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step2_temp1
			);
			$form['step2_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step2_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step2_comment_add_more_callback',
					'wrapper' => 'step2-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step2_num_comment'] > 1)
			{
				$form['step2_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step2_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step2_comment_add_more_callback',
						'wrapper' => 'step2-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step2_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step2_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step2_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step2_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step2_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step2_form_next_submit'
				)
			);
		} //$step2_data = $form_step2_data->fetchObject()
		else
		{
			$form['step2_field1_fieldset']['step2_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step2_field1_fieldset']['step2_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#required' => true
			);
			$form['step2_field1_fieldset']['step2_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not?',
				'#type' => 'textarea',
				'#states' => array(
					'visible' => array(
						':input[name="step2_field1_fieldset\\[step2_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step2_num_comment']))
			{
				$form_state['step2_num_comment'] = 1;
			} //empty($form_state['step2_num_comment'])
			$step2_temp1 = 0;
			for ($step2_i = 0; $step2_i < $form_state['step2_num_comment']; $step2_i++)
			{
				$step2_temp1 = $step2_i;
				$form['step2_field1_fieldset'][$step2_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step2_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step2_field1_fieldset']["step2_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step2_temp1
			);
			$form['step2_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step2_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step2_comment_add_more_callback',
					'wrapper' => 'step2-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step2_num_comment'] > 1)
			{
				$form['step2_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step2_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step2_comment_add_more_callback',
						'wrapper' => 'step2-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step2_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step2_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step2_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step2_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step2_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step2_form_next_submit'
				)
			);
		} //$step2_data = $form_step2_data->fetchObject()
	} //$form_step2_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step2_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step2_field1_fieldset']['step2_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step2_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step2_feedback');
	$query->condition('uid', $user->uid);
	$form_step2_data = $query->execute()->fetchObject();
	if ($form_step2_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step2_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => 'question 1',
			":question_ok_not_ok" => $v['step2_field1_fieldset']['step2_field1_question_ok'],
			":question_not_ok_comment" => $v['step2_field1_fieldset']['step2_field1_question_not_ok_comment'],
			":data_relation" => "step2"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step2_data->id
		));
		$form_step2_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++)
		{
			if ($v['step2_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step2_data->id,
					":number" => $i + $form_step2_comment_data->max + 1,
					":comment" => $v['step2_field1_fieldset'][$i]["comment"],
					":data_relation" => "step2",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step2_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++
	} //$form_step2_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step2_feedback} (uid, question1,question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,:question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step2_field1_fieldset']['step2_field1_question1'],
			":question_ok_not_ok" => $v['step2_field1_fieldset']['step2_field1_question_ok'],
			":question_not_ok_comment" => $v['step2_field1_fieldset']['step2_field1_question_not_ok_comment'],
			":data_relation" => "step2",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++)
		{
			if ($v['step2_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step2_field1_fieldset'][$i]["comment"],
					":data_relation" => "step2",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step2_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step1/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step2_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step2_field1_fieldset']['step2_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step2_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step2_feedback');
	$query->condition('uid', $user->uid);
	$form_step2_data = $query->execute()->fetchObject();
	if ($form_step2_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step2_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => 'question 1',
			":question_ok_not_ok" => $v['step2_field1_fieldset']['step2_field1_question_ok'],
			":question_not_ok_comment" => $v['step2_field1_fieldset']['step2_field1_question_not_ok_comment'],
			":data_relation" => "step2"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step2_data->id
		));
		$form_step2_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++)
		{
			if ($v['step2_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step2_data->id,
					":number" => $i + $form_step2_comment_data->max + 1,
					":comment" => $v['step2_field1_fieldset'][$i]["comment"],
					":data_relation" => "step2",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step2_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++
	} //$form_step2_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step2_feedback} (uid, question1,question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,:question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step2_field1_fieldset']['step2_field1_question1'],
			":question_ok_not_ok" => $v['step2_field1_fieldset']['step2_field1_question_ok'],
			":question_not_ok_comment" => $v['step2_field1_fieldset']['step2_field1_question_not_ok_comment'],
			":data_relation" => "step2",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++)
		{
			if ($v['step2_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step2_field1_fieldset'][$i]["comment"],
					":data_relation" => "step2",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step2_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step2_field1_fieldset']["step2_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step3/' . $user->uid;
}
/***************************************/
/***************************************/
function step2_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step2_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step2_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step2_num_comment'] > 1)
	{
		$form_state['step2_num_comment']--;
	} //$form_state['step3_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step2_comment_add_more_callback($form, &$form_state)
{
	return $form['step2_field1_fieldset'];
}
/***************************************** step 3 form starts **************************/
function ddcl_bb_splice_cover_plate_bolted_step3_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('b. Moment  > i. Moment due to factored axial force > 	ii. Total moment '));
	$markup_text = '
	<b> <strong> b. Moment </strong></b> <br>
	&emsp; <b> <strong> i. Moment due to factored axial force </strong></b> <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
			  <msub>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>M</mi>
			    </mrow>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mtext>F</mtext>
			    </mrow>
			  </msub>
			  <mo>=</mo>
			  <mrow class="MJX-TeXAtom-ORD">
			    <mi>F</mi>
			  </mrow>
			  <mo>&#x00D7;<!-- × --></mo>
			  <mrow class="MJX-TeXAtom-ORD">
			    <mi>C</mi>
			    <mi>G</mi>
			  </mrow>
			</math>

			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
			  <mrow class="MJX-TeXAtom-ORD">
			    <mi>C</mi>
			    <mi>G</mi>
			  </mrow>
			  <mo>=</mo>
			  <mfrac>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>D</mi>
			    </mrow>
			    <mn>2</mn>
			  </mfrac>
			  <mo>&#x2212;<!-- − --></mo>
			  <mfrac>
			    <msub>
			      <mrow class="MJX-TeXAtom-ORD">
			        <mi>t</mi>
			      </mrow>
			      <mrow class="MJX-TeXAtom-ORD">
			        <mtext>f</mtext>
			      </mrow>
			    </msub>
			    <mn>2</mn>
			  </mfrac>
			</math>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <mi>F</mi>
						</math> = Factored axial force  <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;	
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>C</mi>
 							<mi>G</mi>
						</math> = Centroidal distance <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;	
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <mi>D</mi>
						</math> = Overall depth of the beam section <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;	
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>t</mi>
						    <mtext>f</mtext>
						  </msub>
						</math> = Thickness of flange <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<strong> Assumption :</strong> Axial force acts exactly at the center of the section
					<br> <br>

	&emsp; <b> <strong> ii. Total moment  </strong></b> <br>

					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
					  <msub>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mi>M</mi>
					    </mrow>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>T</mtext>
					    </mrow>
					  </msub>
					  <mo>=</mo>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mi>M</mi>
					  </mrow>
					  <mo>+</mo>
					  <msub>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mi>M</mi>
					    </mrow>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>F</mtext>
					    </mrow>
					  </msub>
					</math>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <mi>M</mi>
						</math> = Factored moment <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>M</mi>
						    <mtext>F</mtext>
						  </msub>
						</math> = Moment due to factored axial force <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<strong> Note :</strong> <math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>M</mi>
						    <mtext>F</mtext>
						  </msub>
						</math> = 0, if axial force is not considered <br>
	';
	$markup_text1 = '';
	$tooltip1 = '';
	// All the real form fields.
	$form = array();
	$form['step3_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step3-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step3_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step3_feedback');
	$query->condition('uid', $user->uid);
	$form_step3_data = $query->execute();
	if ($form_step3_data)
	{
		if ($step3_data = $form_step3_data->fetchObject())
		{
			$form['step3_field1_fieldset']['step3_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step3_field1_fieldset']['tooltip1'] = array(
				'#type' => 'fieldset',
				'#title' => $tooltip1,
				'#collapsible' => TRUE, // Added
				'#collapsed' => TRUE // Added
			);
			$form['step3_field1_fieldset']['tooltip1']['tooltip1_text'] = array(
				'#markup' => $markup_text1
			);
			$form['step3_field1_fieldset']['step3_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step3_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step3_field1_fieldset']['step3_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not?',
				'#type' => 'textarea',
				'#default_value' => $step3_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step3_field1_fieldset\\[step3_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step3_data->id, $step3_data->data_relation);
			$icom = 1;
			$form['step3_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr><strong>Earlier comment</strong><hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step3_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step3_num_comment']))
			{
				$form_state['step3_num_comment'] = 1;
			} //empty($form_state['step3_num_comment'])
			$step3_temp1 = 0;
			for ($step3_i = 0; $step3_i < $form_state['step3_num_comment']; $step3_i++)
			{
				$step3_temp1 = $step3_i;
				$form['step3_field1_fieldset'][$step3_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step3_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step3_field1_fieldset']["step3_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step3_temp1
			);
			$form['step3_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step3_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step3_comment_add_more_callback',
					'wrapper' => 'step3-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step3_num_comment'] > 1)
			{
				$form['step3_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step3_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step3_comment_add_more_callback',
						'wrapper' => 'step3-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step3_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step3_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step3_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step3_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form['previous2'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step3_form_previous_submit'
				)
			);
			$form['next3'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step3_form_next_submit'
				)
			);
		} //$step3_data = $form_step3_data->fetchObject()
		else
		{
			$form['step3_field1_fieldset']['step3_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step3_field1_fieldset']['step3_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#required' => true
			);
			$form['step3_field1_fieldset']['step3_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not?',
				'#type' => 'textarea',
				'#states' => array(
					'visible' => array(
						':input[name="step3_field1_fieldset\\[step3_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step3_num_comment']))
			{
				$form_state['step3_num_comment'] = 1;
			} //empty($form_state['step3_num_comment'])
			$step3_temp1 = 0;
			for ($step3_i = 0; $step3_i < $form_state['step3_num_comment']; $step3_i++)
			{
				$step3_temp1 = $step3_i;
				$form['step3_field1_fieldset'][$step3_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step3_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step3_field1_fieldset']["step3_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step3_temp1
			);
			$form['step3_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step3_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step3_comment_add_more_callback',
					'wrapper' => 'step3-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step3_num_comment'] > 1)
			{
				$form['step3_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step3_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step3_comment_add_more_callback',
						'wrapper' => 'step3-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step3_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step3_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step3_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step3_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step3_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step3_form_next_submit'
				)
			);
		} //$step3_data = $form_step3_data->fetchObject()
	} //$form_step3_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step3_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step3_field1_fieldset']['step3_field1_question1'] = 'question 3';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step3_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step3_feedback');
	$query->condition('uid', $user->uid);
	$form_step3_data = $query->execute()->fetchObject();
	//var_dump($form_step2_data);die;
	if ($form_step3_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step3_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step3_field1_fieldset']['step3_field1_question1'],
			":question_ok_not_ok" => $v['step3_field1_fieldset']['step3_field1_question_ok'],
			":question_not_ok_comment" => $v['step3_field1_fieldset']['step3_field1_question_not_ok_comment'],
			":data_relation" => "step3"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step3_data->id
		));
		$form_step3_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++)
		{
			if ($v['step3_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step3_data->id,
					":number" => $i + $form_step3_comment_data->max + 1,
					":comment" => $v['step3_field1_fieldset'][$i]["comment"],
					":data_relation" => "step3",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step3_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++
	} //$form_step2_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step3_feedback} (uid, question1,question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step3_field1_fieldset']['step3_field1_question1'],
			":question_ok_not_ok" => $v['step3_field1_fieldset']['step3_field1_question_ok'],
			":question_not_ok_comment" => $v['step3_field1_fieldset']['step3_field1_question_not_ok_comment'],
			":data_relation" => "step3",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++)
		{
			if ($v['step3_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step3_field1_fieldset'][$i]["comment"],
					":data_relation" => "step3",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step3_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step2/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step3_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step3_field1_fieldset']['step3_field1_question1'] = 'question 3';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step3_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step3_feedback');
	$query->condition('uid', $user->uid);
	$form_step3_data = $query->execute()->fetchObject();
	//var_dump($form_step2_data);die;
	if ($form_step3_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step3_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step3_field1_fieldset']['step3_field1_question1'],
			":question_ok_not_ok" => $v['step3_field1_fieldset']['step3_field1_question_ok'],
			":question_not_ok_comment" => $v['step3_field1_fieldset']['step3_field1_question_not_ok_comment'],
			":data_relation" => "step3"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step3_data->id
		));
		$form_step3_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++)
		{
			if ($v['step3_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step3_data->id,
					":number" => $i + $form_step3_comment_data->max + 1,
					":comment" => $v['step3_field1_fieldset'][$i]["comment"],
					":data_relation" => "step3",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step3_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++
	} //$form_step2_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step3_feedback} (uid, question1,question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step3_field1_fieldset']['step3_field1_question1'],
			":question_ok_not_ok" => $v['step3_field1_fieldset']['step3_field1_question_ok'],
			":question_not_ok_comment" => $v['step3_field1_fieldset']['step3_field1_question_not_ok_comment'],
			":data_relation" => "step3",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++)
		{
			if ($v['step3_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step3_field1_fieldset'][$i]["comment"],
					":data_relation" => "step3",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step3_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step3_field1_fieldset']["step3_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step4/' . $user->uid;
}
/***************************************/
function step3_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step3_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step3_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step3_num_comment'] > 1)
	{
		$form_state['step3_num_comment']--;
	} //$form_state['step3_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step3_comment_add_more_callback($form, &$form_state)
{
	return $form['step3_field1_fieldset'];
}
/***************************************/
/***************************************** step 3 form ends **************************/
/************************ Step 4 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step4_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('c. Force in  flange'));
	$img_path = $base_url . '/' . drupal_get_path("module", "osdag_response_form") . '/images';
	$markup_text = '
	<b> <strong> c. Force in  flange </strong> [Reference: M.L. Gambhir (page 10.83), N. Subramanian (page 427)]</b> <br>
			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>F</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>F</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <msub>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mi>M</mi>
				      </mrow>
				      <mtext>T</mtext>
				    </msub>
				    <mrow>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mi>D</mi>
				      </mrow>
				      <mo>&#x2212;<!-- − --></mo>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>t</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>f</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				</math>
				</p>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>F</mi>
						    <mtext>F</mtext>
						  </msub>
						</math> = Force in flange  <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;	
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						   <msub>
						    <mi>M</mi>
						    <mtext>T</mtext>
						  </msub>
						</math> = Total moment acting on the connection <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;	
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <mi>D</mi>
						</math> = Overall depth of the beam section <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;	
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>t</mi>
						    <mtext>f</mtext>
						  </msub>
						</math> = Thickness of flange <br> <hr>
						&emsp;&emsp;&emsp;&emsp;&emsp;				
				<img src="' . $img_path . '/BBSpliceFlangeForce.jpg" width="70%" height="60%" align="middle" />
				<br>
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
				Figure: Formula to calculate force in flange [Reference: N. Subramanian, Page 427]
				<br>

	<hr>';
	// All the real form fields.
	$form = array();
	$form['step4_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step4-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step4_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step4_feedback');
	$query->condition('uid', $user->uid);
	$form_step4_data = $query->execute();
	if ($form_step4_data)
	{
		if ($step4_data = $form_step4_data->fetchObject())
		{
			$form['step4_field1_fieldset']['step4_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step4_field1_fieldset']['step4_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step4_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step4_field1_fieldset']['step4_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step4_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step4_field1_fieldset\\[step4_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step4_data->id, $step4_data->data_relation);
			$icom = 1;
			$form['step4_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr>Earlier comment<hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step4_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step4_num_comment']))
			{
				$form_state['step4_num_comment'] = 1;
			} //empty($form_state['step4_num_comment'])
			$step4_temp1 = 0;
			for ($step4_i = 0; $step4_i < $form_state['step4_num_comment']; $step4_i++)
			{
				$step4_temp1 = $step4_i;
				$form['step4_field1_fieldset'][$step4_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step4_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step4_field1_fieldset']["step4_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step4_temp1
			);
			$form['step4_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step4_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step4_comment_add_more_callback',
					'wrapper' => 'step4-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step4_num_comment'] > 1)
			{
				$form['step4_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step4_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step4_comment_add_more_callback',
						'wrapper' => 'step4-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step4_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step4_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step4_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step4_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step4_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step4_form_next_submit'
				)
			);
		} //$step4_data = $form_step4_data->fetchObject()
		else
		{
			$form['step4_field1_fieldset']['step4_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step4_field1_fieldset']['step4_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#required' => true
			);
			$form['step4_field1_fieldset']['step4_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#states' => array(
					'visible' => array(
						':input[name="step4_field1_fieldset\\[step4_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step4_num_comment']))
			{
				$form_state['step4_num_comment'] = 1;
			} //empty($form_state['step4_num_comment'])
			$step4_temp1 = 0;
			for ($step4_i = 0; $step4_i < $form_state['step4_num_comment']; $step4_i++)
			{
				$step4_temp1 = $step4_i;
				$form['step4_field1_fieldset'][$step4_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step4_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step4_field1_fieldset']["step4_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step4_temp1
			);
			$form['step4_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step4_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step4_comment_add_more_callback',
					'wrapper' => 'step4-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step4_num_comment'] > 1)
			{
				$form['step4_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step4_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step4_comment_add_more_callback',
						'wrapper' => 'step4-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step4_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step4_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step4_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step4_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step4_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step4_form_next_submit'
				)
			);
		} //$step4_data = $form_step4_data->fetchObject()
	} //$form_step4_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step4_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step4_field1_fieldset']['step4_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step4_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step4_feedback');
	$query->condition('uid', $user->uid);
	$form_step4_data = $query->execute()->fetchObject();
	//var_dump($form_step4_data);die;
	if ($form_step4_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step4_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step4_field1_fieldset']['step4_field1_question1'],
			":question_ok_not_ok" => $v['step4_field1_fieldset']['step4_field1_question_ok'],
			":question_not_ok_comment" => $v['step4_field1_fieldset']['step4_field1_question_not_ok_comment'],
			":data_relation" => "step4"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step4_data->id
		));
		$form_step4_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++)
		{
			if ($v['step4_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step4_data->id,
					":number" => $i + $form_step4_comment_data->max + 1,
					":comment" => $v['step4_field1_fieldset'][$i]["comment"],
					":data_relation" => "step4",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step4_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++
	} //$form_step4_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step4_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step4_field1_fieldset']['step4_field1_question1'],
			":question_ok_not_ok" => $v['step4_field1_fieldset']['step4_field1_question_ok'],
			":question_not_ok_comment" => $v['step4_field1_fieldset']['step4_field1_question_not_ok_comment'],
			":data_relation" => "step4",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++)
		{
			if ($v['step4_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step4_field1_fieldset'][$i]["comment"],
					":data_relation" => "step4",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step4_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step3/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step4_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step4_field1_fieldset']['step4_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step4_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step4_feedback');
	$query->condition('uid', $user->uid);
	$form_step4_data = $query->execute()->fetchObject();
	//var_dump($form_step4_data);die;
	if ($form_step4_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step4_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step4_field1_fieldset']['step4_field1_question1'],
			":question_ok_not_ok" => $v['step4_field1_fieldset']['step4_field1_question_ok'],
			":question_not_ok_comment" => $v['step4_field1_fieldset']['step4_field1_question_not_ok_comment'],
			":data_relation" => "step4"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step4_data->id
		));
		$form_step4_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++)
		{
			if ($v['step4_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step4_data->id,
					":number" => $i + $form_step4_comment_data->max + 1,
					":comment" => $v['step4_field1_fieldset'][$i]["comment"],
					":data_relation" => "step4",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step4_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++
	} //$form_step4_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step4_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step4_field1_fieldset']['step4_field1_question1'],
			":question_ok_not_ok" => $v['step4_field1_fieldset']['step4_field1_question_ok'],
			":question_not_ok_comment" => $v['step4_field1_fieldset']['step4_field1_question_not_ok_comment'],
			":data_relation" => "step4",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++)
		{
			if ($v['step4_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step4_field1_fieldset'][$i]["comment"],
					":data_relation" => "step4",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step4_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step4_field1_fieldset']["step4_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step5/' . $user->uid;
}
/***************************************/
function step4_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step4_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step4_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step4_num_comment'] > 1)
	{
		$form_state['step4_num_comment']--;
	} //$form_state['step4_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step4_comment_add_more_callback($form, &$form_state)
{
	return $form['step4_field1_fieldset'];
}
/***************************************/
/***************************************** step 4 from ends ****************************/
/************************ Step 5 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step5_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of flange splice plate > d. Bolt > i. Shear capacity of bearing bolt'));
	$markup_text = '
	<b> <strong> d. Bolt </strong> </b> <br>
	&emsp; <b> <strong> i. Shear capacity of bearing bolt </strong> [Reference: Clause 10.3.3 page 75, IS 800 : 2007] </b> <br>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dsb</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>u</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <mo stretchy="false">(</mo>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>n</mi>
				        </mrow>
				        <mtext>n</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>nb</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <mo>+</mo>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>n</mi>
				        </mrow>
				        <mtext>s</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>sb</mtext>
				        </mrow>
				      </msub>
				      <mo stretchy="false">)</mo>
				    </mrow>
				    <mrow>
				      <msqrt>
				        <mn>3</mn>
				      </msqrt>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mi>&#x03B3;<!-- γ --></mi>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>mb</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				</math>

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dsb</mtext>
						  </msub>
						</math> = Design shear capacity of bolt  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>u</mtext>
						  </msub>
						</math> = Characteristic ultimate tensile stress  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						<msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>mb</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor for bolted connection with bearing type bolts  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>n</mi>
						    <mtext>n</mtext>
						  </msub>
						</math> = Number of shear planes with threads intercepting the shear plane  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mtext>nb</mtext>
						  </msub>
						</math> = Net shear area of the bolt at threads [Table 5.11 N. Subramanian]  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>n</mi>
						    <mtext>s</mtext>
						  </msub>
						</math> = Number of shear planes without threads intercepting the shear plane  <br>	
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mtext>sb</mtext>
						  </msub>
						</math> = Nominal plain shank area of the bolt  <br>

	&emsp;&emsp;&emsp; <strong> This step is same as implemented in the shear connection modules (already reviewed). </strong>
	<br>
		
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step5_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step5-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step5_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step5_feedback');
	$query->condition('uid', $user->uid);
	$form_step5_data = $query->execute();
	if ($form_step5_data)
	{
		if ($step5_data = $form_step5_data->fetchObject())
		{
			$form['step5_field1_fieldset']['step5_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step5_field1_fieldset']['step5_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step5_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step5_field1_fieldset']['step5_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step5_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step5_field1_fieldset\\[step5_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step5_data->id, $step5_data->data_relation);
			$icom = 1;
			$form['step5_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr><strong>Earlier comment</strong><hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step5_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step5_num_comment']))
			{
				$form_state['step5_num_comment'] = 1;
			} //empty($form_state['step5_num_comment'])
			$step5_temp1 = 0;
			for ($step5_i = 0; $step5_i < $form_state['step5_num_comment']; $step5_i++)
			{
				$step5_temp1 = $step5_i;
				$form['step5_field1_fieldset'][$step5_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step5_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step5_field1_fieldset']["step5_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step5_temp1
			);
			$form['step5_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step5_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step5_comment_add_more_callback',
					'wrapper' => 'step5-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step5_num_comment'] > 1)
			{
				$form['step5_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step5_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step5_comment_add_more_callback',
						'wrapper' => 'step5-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step5_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step5_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step5_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step5_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step5_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step5_form_next_submit'
				)
			);
		} //$step5_data = $form_step5_data->fetchObject()
		else
		{
			$form['step5_field1_fieldset']['step5_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step5_field1_fieldset']['step5_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step2_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step5_field1_fieldset']['step5_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step5_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step5_field1_fieldset\\[step5_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step5_num_comment']))
			{
				$form_state['step5_num_comment'] = 1;
			} //empty($form_state['step5_num_comment'])
			$step5_temp1 = 0;
			for ($step5_i = 0; $step5_i < $form_state['step5_num_comment']; $step5_i++)
			{
				$step5_temp1 = $step5_i;
				$form['step5_field1_fieldset'][$step5_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step5_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step5_field1_fieldset']["step5_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step5_temp1
			);
			$form['step5_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step5_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step5_comment_add_more_callback',
					'wrapper' => 'step5-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step5_num_comment'] > 1)
			{
				$form['step5_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step5_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step5_comment_add_more_callback',
						'wrapper' => 'step5-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step5_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step5_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step5_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step5_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step5_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step5_form_next_submit'
				)
			);
		} //$step5_data = $form_step5_data->fetchObject()
	} //$form_step5_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step5_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step5_field1_fieldset']['step5_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step5_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step5_feedback');
	$query->condition('uid', $user->uid);
	$form_step5_data = $query->execute()->fetchObject();
	//var_dump($form_step5_data);die;
	if ($form_step5_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step5_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step5_field1_fieldset']['step5_field1_question1'],
			":question_ok_not_ok" => $v['step5_field1_fieldset']['step5_field1_question_ok'],
			":question_not_ok_comment" => $v['step5_field1_fieldset']['step5_field1_question_not_ok_comment'],
			":data_relation" => "step5"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step5_data->id
		));
		$form_step5_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++)
		{
			if ($v['step5_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step5_data->id,
					":number" => $i + $form_step5_comment_data->max + 1,
					":comment" => $v['step5_field1_fieldset'][$i]["comment"],
					":data_relation" => "step5",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step5_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++
	} //$form_step5_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step5_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation, inserted_on) VALUES (:uid, :question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step5_field1_fieldset']['step5_field1_question1'],
			":question_ok_not_ok" => $v['step5_field1_fieldset']['step5_field1_question_ok'],
			":question_not_ok_comment" => $v['step5_field1_fieldset']['step5_field1_question_not_ok_comment'],
			":data_relation" => "step5",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++)
		{
			if ($v['step5_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step5_field1_fieldset'][$i]["comment"],
					":data_relation" => "step5",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step5_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step4/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step5_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step5_field1_fieldset']['step5_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step5_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step5_feedback');
	$query->condition('uid', $user->uid);
	$form_step5_data = $query->execute()->fetchObject();
	//var_dump($form_step5_data);die;
	if ($form_step5_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step5_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step5_field1_fieldset']['step5_field1_question1'],
			":question_ok_not_ok" => $v['step5_field1_fieldset']['step5_field1_question_ok'],
			":question_not_ok_comment" => $v['step5_field1_fieldset']['step5_field1_question_not_ok_comment'],
			":data_relation" => "step5"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step5_data->id
		));
		$form_step5_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++)
		{
			if ($v['step5_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step5_data->id,
					":number" => $i + $form_step5_comment_data->max + 1,
					":comment" => $v['step5_field1_fieldset'][$i]["comment"],
					":data_relation" => "step5",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step5_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++
	} //$form_step5_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step5_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation, inserted_on) VALUES (:uid, :question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step5_field1_fieldset']['step5_field1_question1'],
			":question_ok_not_ok" => $v['step5_field1_fieldset']['step5_field1_question_ok'],
			":question_not_ok_comment" => $v['step5_field1_fieldset']['step5_field1_question_not_ok_comment'],
			":data_relation" => "step5",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++)
		{
			if ($v['step5_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step5_field1_fieldset'][$i]["comment"],
					":data_relation" => "step5",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step5_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step5_field1_fieldset']["step5_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step6/' . $user->uid;
}
/***************************************/
function step5_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step5_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step5_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step5_num_comment'] > 1)
	{
		$form_state['step5_num_comment']--;
	} //$form_state['step5_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step5_comment_add_more_callback($form, &$form_state)
{
	return $form['step5_field1_fieldset'];
}
/***************************************/
/***************************************** step 5 from ends ****************************/
/************************ Step 6 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step6_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of flange splice > d. Bolt > ii. Shear capacacity / Slip resistance of HSFG bolt'));
	$markup_text = '
	<b> <strong> d. Bolt </strong> </b> <br>
	&emsp; <b> <strong> ii. Shear capacity / Slip resistance of HSFG bolt </strong> [Reference: Clause 10.4.3 page 76, IS 800 : 2007] </b> <br>

	<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <msub>
    <mrow class="MJX-TeXAtom-ORD">
      <mi>V</mi>
    </mrow>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>dsf</mtext>
    </mrow>
  </msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <msub>
        <mi>&#x03BC;<!-- μ --></mi>
        <mtext>f</mtext>
      </msub>
      <mspace width="thinmathspace" />
      <mspace width="thinmathspace" />
      <msub>
        <mrow class="MJX-TeXAtom-ORD">
          <mi>n</mi>
        </mrow>
        <mtext>e</mtext>
      </msub>
      <mspace width="thinmathspace" />
      <msub>
        <mrow class="MJX-TeXAtom-ORD">
          <mi>K</mi>
        </mrow>
        <mtext>h</mtext>
      </msub>
      <mspace width="thinmathspace" />
      <msub>
        <mrow class="MJX-TeXAtom-ORD">
          <mi>F</mi>
        </mrow>
        <mn>0</mn>
      </msub>
    </mrow>
    <msub>
      <mi>&#x03B3;<!-- γ --></mi>
      <mrow class="MJX-TeXAtom-ORD">
        <mtext>mf</mtext>
      </mrow>
    </msub>
  </mfrac>
</math>

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dsf</mtext>
						  </msub>
						</math> = Design shear capacity of a HSFG bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03BC;<!-- μ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>f</mtext>
						    </mrow>
						  </msub>
						</math> = Coefficient of friction (slip factor)  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>n</mi>
						    <mtext>e</mtext>
						  </msub>
						</math> = Number of effective interfaces offering frictional resistance to slip  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>mf</mtext>
						    </mrow>
						  </msub>
						</math> = 1.10 if slip resistance is designed at service load <br>
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; = 1.25 if slip resistance is designed at ultimate load	 <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>K</mi>
						    <mtext>h</mtext>
						  </msub>
						</math> = 1.0 for fasteners in clearance hole  <br>
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; = 0.85 for fasteners in oversized and short slotted holes <br>
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; = 0.7 for fasteners in long slotted holes loaded parallel to the slot <br> 
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>F</mi>
						    <mtext>0</mtext>
						  </msub>
						</math> = Minimum bolt tension (proof load) at installation and may be taken as 
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						 <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>nb</mtext>
						    </mrow>
						  </msub>
						  <mspace width="thinmathspace" />
						  <msub>
						    <mi>f</mi>
						    <mn>0</mn>
						  </msub>  <br>
						  </math>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mtext>nb</mtext>
						  </msub>
						</math> = Net area of the bolt at threads [Table 5.11 N. Subramanian]  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">						  
						    <mi>d</mi>				
						</math> = Diameter of the bolt  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>0</mtext>
						  </msub>
						</math> =  Proof stress   <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>ub</mtext>
						  </msub>
						</math> = Characteristic ultimate tensile stress of the bolt  <br>

	&emsp;&emsp;&emsp; <strong> This step is same as implemented in the shear connection modules (already reviewed). </strong>
	<br> 
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step6_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step6-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step6_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step6_feedback');
	$query->condition('uid', $user->uid);
	$form_step6_data = $query->execute();
	if ($form_step6_data)
	{
		if ($step6_data = $form_step6_data->fetchObject())
		{
			$form['step6_field1_fieldset']['step6_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step6_field1_fieldset']['step6_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step6_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step6_field1_fieldset']['step6_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step6_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step6_field1_fieldset\\[step6_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step6_data->id, $step6_data->data_relation);
			$icom = 1;
			$form['step6_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr>Earlier comment<hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step6_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step6_num_comment']))
			{
				$form_state['step6_num_comment'] = 1;
			} //empty($form_state['step6_num_comment'])
			$step6_temp1 = 0;
			for ($step6_i = 0; $step6_i < $form_state['step6_num_comment']; $step6_i++)
			{
				$step6_temp1 = $step6_i;
				$form['step6_field1_fieldset'][$step6_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step6_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step6_field1_fieldset']["step6_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step6_temp1
			);
			$form['step6_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step6_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step6_comment_add_more_callback',
					'wrapper' => 'step6-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step6_num_comment'] > 1)
			{
				$form['step6_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step6_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step6_comment_add_more_callback',
						'wrapper' => 'step6-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step6_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step6_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step6_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step6_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step6_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step6_form_next_submit'
				)
			);
		} //$step6_data = $form_step6_data->fetchObject()
		else
		{
			$form['step6_field1_fieldset']['step6_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step6_field1_fieldset']['step6_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok?</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step6_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step6_field1_fieldset']['step6_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step6_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step6_field1_fieldset\\[step6_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step6_num_comment']))
			{
				$form_state['step6_num_comment'] = 1;
			} //empty($form_state['step6_num_comment'])
			$step6_temp1 = 0;
			for ($step6_i = 0; $step6_i < $form_state['step6_num_comment']; $step6_i++)
			{
				$step6_temp1 = $step6_i;
				$form['step6_field1_fieldset'][$step6_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step6_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step6_field1_fieldset']["step6_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step6_temp1
			);
			$form['step6_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step6_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step6_comment_add_more_callback',
					'wrapper' => 'step6-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step6_num_comment'] > 1)
			{
				$form['step6_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step6_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step6_comment_add_more_callback',
						'wrapper' => 'step6-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step6_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step6_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step6_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step6_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step6_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step6_form_next_submit'
				)
			);
		} //$step6_data = $form_step6_data->fetchObject()
	} //$form_step6_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step6_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step6_field1_fieldset']['step6_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step6_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step6_feedback');
	$query->condition('uid', $user->uid);
	$form_step6_data = $query->execute()->fetchObject();
	//var_dump($form_step6_data);die;
	if ($form_step6_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step6_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step6_field1_fieldset']['step6_field1_question1'],
			":question_ok_not_ok" => $v['step6_field1_fieldset']['step6_field1_question_ok'],
			":question_not_ok_comment" => $v['step6_field1_fieldset']['step6_field1_question_not_ok_comment'],
			":data_relation" => "step6"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step6_data->id
		));
		$form_step6_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++)
		{
			if ($v['step6_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step6_data->id,
					":number" => $i + $form_step6_comment_data->max + 1,
					":comment" => $v['step6_field1_fieldset'][$i]["comment"],
					":data_relation" => "step6",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step6_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++
	} //$form_step6_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step6_feedback} (uid, question1, question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step6_field1_fieldset']['step6_field1_question1'],
			":question_ok_not_ok" => $v['step6_field1_fieldset']['step6_field1_question_ok'],
			":question_not_ok_comment" => $v['step6_field1_fieldset']['step6_field1_question_not_ok_comment'],
			":data_relation" => "step6",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++)
		{
			if ($v['step6_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step6_field1_fieldset'][$i]["comment"],
					":data_relation" => "step6",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step6_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step5/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step6_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step6_field1_fieldset']['step6_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step6_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step6_feedback');
	$query->condition('uid', $user->uid);
	$form_step6_data = $query->execute()->fetchObject();
	//var_dump($form_step6_data);die;
	if ($form_step6_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step6_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step6_field1_fieldset']['step6_field1_question1'],
			":question_ok_not_ok" => $v['step6_field1_fieldset']['step6_field1_question_ok'],
			":question_not_ok_comment" => $v['step6_field1_fieldset']['step6_field1_question_not_ok_comment'],
			":data_relation" => "step6"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step6_data->id
		));
		$form_step6_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++)
		{
			if ($v['step6_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step6_data->id,
					":number" => $i + $form_step6_comment_data->max + 1,
					":comment" => $v['step6_field1_fieldset'][$i]["comment"],
					":data_relation" => "step6",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step6_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++
	} //$form_step6_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step6_feedback} (uid, question1, question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step6_field1_fieldset']['step6_field1_question1'],
			":question_ok_not_ok" => $v['step6_field1_fieldset']['step6_field1_question_ok'],
			":question_not_ok_comment" => $v['step6_field1_fieldset']['step6_field1_question_not_ok_comment'],
			":data_relation" => "step6",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++)
		{
			if ($v['step6_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step6_field1_fieldset'][$i]["comment"],
					":data_relation" => "step6",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step6_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step6_field1_fieldset']["step6_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step7/' . $user->uid;
}
/***************************************/
function step6_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step6_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step6_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step6_num_comment'] > 1)
	{
		$form_state['step6_num_comment']--;
	} //$form_state['step6_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step6_comment_add_more_callback($form, &$form_state)
{
	return $form['step6_field1_fieldset'];
}
/***************************************/
/***************************************** step 6 from ends ****************************/
/************************ Step 7 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step7_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of flange splice  > d. Bolt > iii. Bearing capacity of Bolt'));
	$markup_text = '
	<b> <strong> d. Bolt </strong> </b> <br>
	&emsp; <b> <strong> iii. Bearing capacity of Bolt </strong> [Reference: Clause 10.3.4 page 75, IS  800 : 2007] </b> <br>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dpb</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <mn>2.5</mn>
				      <mspace width="thinmathspace" />
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>k</mi>
				        </mrow>
				        <mtext>b</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <mi>d</mi>
				      <mspace width="thinmathspace" />
				      <mi>t</mi>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>u</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				    <msub>
				      <mi>&#x03B3;<!-- γ --></mi>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mtext>mb</mtext>
				      </mrow>
				    </msub>
				  </mfrac>
				</math>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dpb</mtext>
						  </msub>
						</math> = Design bearing strength of a bolt <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
					  <msub>
					    <mi>k</mi>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>b</mtext>
					    </mrow>
					  </msub>
					</math>	is smaller of

					<math xmlns="http://www.w3.org/1998/Math/MathML">
					  <mo stretchy="false">(</mo>
					  <mi>e</mi>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo>/</mo>
					  </mrow>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mn>3</mn>
					    <msub>
					      <mi>d</mi>
					      <mn>0</mn>
					    </msub>
					  </mrow>
					  <mo stretchy="false">)</mo>
					  <mo>,</mo>
					  <mo stretchy="false">(</mo>
					  <mi>p</mi>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo>/</mo>
					  </mrow>
					  <mn>3</mn>
					  <msub>
					    <mi>d</mi>
					    <mn>0</mn>
					  </msub>
					  <mo stretchy="false">)</mo>
					  <mo>,</mo>
					  <mo stretchy="false">(</mo>
					  <msub>
					    <mi>f</mi>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>ub</mtext>
					    </mrow>
					  </msub>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo>/</mo>
					  </mrow>
					  <msub>
					    <mi>f</mi>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>u</mtext>
					    </mrow>
					  </msub>
					  <mo stretchy="false">)</mo>
					  <mo>,</mo>
					  <mn>1.0</mn>
					</math> <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
					   <mi>e, p</mi>
					</math> = End and pitch distances of the fastener along bearing direction <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>d</mi>
						    <mtext>0</mtext>
						  </msub>
					</math> = Diameter of the bolt hole <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>ub</mtext>
						    </mrow>
						  </msub>
						  <mo>,</mo>
						  <msub>
						    <mi>f</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>u</mtext>
						    </mrow>
						  </msub>
					</math> = Ultimate tensile stress of the bolt and the ultimate tensile stress of the plate <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">						 
						    <mi>d</mi>						
					</math> = Nominal diameter of the bolt <br>
										&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>t</mi>
					</math> = Mimimum(flange thickness, flange splice plate thickne) <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>mb</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor for bolted connection with bearing type bolts <br>
&emsp;&emsp;&emsp; <strong> This step is same as implemented in the shear connection modules (already reviewed). </strong>
	<br>
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step7_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step7-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step7_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step7_feedback');
	$query->condition('uid', $user->uid);
	$form_step7_data = $query->execute();
	if ($form_step7_data)
	{
		if ($step7_data = $form_step7_data->fetchObject())
		{
			$form['step7_field1_fieldset']['step7_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step7_field1_fieldset']['step7_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step7_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step7_field1_fieldset']['step7_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step7_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step7_field1_fieldset\\[step7_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step7_data->id, $step7_data->data_relation);
			$icom = 1;
			$form['step7_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr>Earlier comment<hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step7_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step7_num_comment']))
			{
				$form_state['step7_num_comment'] = 1;
			} //empty($form_state['step7_num_comment'])
			$step7_temp1 = 0;
			for ($step7_i = 0; $step7_i < $form_state['step7_num_comment']; $step7_i++)
			{
				$step7_temp1 = $step7_i;
				$form['step7_field1_fieldset'][$step7_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step7_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step7_field1_fieldset']["step7_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step7_temp1
			);
			$form['step7_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step7_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step7_comment_add_more_callback',
					'wrapper' => 'step7-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step7_num_comment'] > 1)
			{
				$form['step7_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step7_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step7_comment_add_more_callback',
						'wrapper' => 'step7-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step7_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step7_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step7_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step7_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step7_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step7_form_next_submit'
				)
			);
		} //$step7_data = $form_step7_data->fetchObject()
		else
		{
			$form['step7_field1_fieldset']['step7_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step7_field1_fieldset']['step7_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step7_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step7_field1_fieldset']['step7_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step7_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step7_field1_fieldset\\[step7_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step7_num_comment']))
			{
				$form_state['step7_num_comment'] = 1;
			} //empty($form_state['step7_num_comment'])
			$step7_temp1 = 0;
			for ($step7_i = 0; $step7_i < $form_state['step7_num_comment']; $step7_i++)
			{
				$step7_temp1 = $step7_i;
				$form['step7_field1_fieldset'][$step7_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step7_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step7_field1_fieldset']["step7_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step7_temp1
			);
			$form['step7_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step7_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step7_comment_add_more_callback',
					'wrapper' => 'step7-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step7_num_comment'] > 1)
			{
				$form['step7_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step7_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step7_comment_add_more_callback',
						'wrapper' => 'step7-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step7_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step7_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step7_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step7_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step7_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step7_form_next_submit'
				)
			);
		} //$step7_data = $form_step7_data->fetchObject()
	} //$form_step7_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step7_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step7_field1_fieldset']['step7_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step7_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step7_feedback');
	$query->condition('uid', $user->uid);
	$form_step7_data = $query->execute()->fetchObject();
	//var_dump($form_step7_data);die;
	if ($form_step7_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step7_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step7_field1_fieldset']['step7_field1_question1'],
			":question_ok_not_ok" => $v['step7_field1_fieldset']['step7_field1_question_ok'],
			":question_not_ok_comment" => $v['step7_field1_fieldset']['step7_field1_question_not_ok_comment'],
			":data_relation" => "step7"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step7_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++)
		{
			if ($v['step7_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step7_data->id,
					":number" => $i + $form_step7_comment_data->max + 1,
					":comment" => $v['step7_field1_fieldset'][$i]["comment"],
					":data_relation" => "step7",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step7_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++
	} //$form_step7_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step7_feedback} (uid, question1,question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step7_field1_fieldset']['step7_field1_question1'],
			":question_ok_not_ok" => $v['step7_field1_fieldset']['step7_field1_question_ok'],
			":question_not_ok_comment" => $v['step7_field1_fieldset']['step7_field1_question_not_ok_comment'],
			":data_relation" => "step7",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++)
		{
			if ($v['step7_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step7_field1_fieldset'][$i]["comment"],
					":data_relation" => "step7",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step7_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step6/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step7_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step7_field1_fieldset']['step7_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step7_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step7_feedback');
	$query->condition('uid', $user->uid);
	$form_step7_data = $query->execute()->fetchObject();
	//var_dump($form_step7_data);die;
	if ($form_step7_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step7_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step7_field1_fieldset']['step7_field1_question1'],
			":question_ok_not_ok" => $v['step7_field1_fieldset']['step7_field1_question_ok'],
			":question_not_ok_comment" => $v['step7_field1_fieldset']['step7_field1_question_not_ok_comment'],
			":data_relation" => "step7"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step7_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++)
		{
			if ($v['step7_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step7_data->id,
					":number" => $i + $form_step7_comment_data->max + 1,
					":comment" => $v['step7_field1_fieldset'][$i]["comment"],
					":data_relation" => "step7",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step7_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++
	} //$form_step7_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step7_feedback} (uid, question1,question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step7_field1_fieldset']['step7_field1_question1'],
			":question_ok_not_ok" => $v['step7_field1_fieldset']['step7_field1_question_ok'],
			":question_not_ok_comment" => $v['step7_field1_fieldset']['step7_field1_question_not_ok_comment'],
			":data_relation" => "step7",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++)
		{
			if ($v['step7_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step7_field1_fieldset'][$i]["comment"],
					":data_relation" => "step7",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step7_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step7_field1_fieldset']["step7_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step8/' . $user->uid;
}
/***************************************/
function step7_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step7_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step7_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step7_num_comment'] > 1)
	{
		$form_state['step7_num_comment']--;
	} //$form_state['step7_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step7_comment_add_more_callback($form, &$form_state)
{
	return $form['step7_field1_fieldset'];
}
/***************************************/
/***************************************** step 7 from ends ****************************/
/************************ Step 8 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step8_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of flange splice > d. Bolt > iv. Bolt value > v. Number of bolts'));
	$img_path = $base_url . '/' . drupal_get_path("module", "osdag_response_form") . '/images';
	$markup_text = '
	<b> <strong> d. Bolt </strong></b> <br>
	&emsp; <b> <strong> iv. Bolt value </strong> <br>
	&emsp;&emsp;			The bolt value is taken as the minimum of bolt shear and bolt bearing capacity.
			  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mi>V</mi>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mtext>min</mtext>
				  <mo stretchy="false">(</mo>
				  <msub>
				    <mi>V</mi>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dsb</mtext>
				    </mrow>
				  </msub>
				  <mo>,</mo>
				  <mspace width="thinmathspace" />
				  <msub>
				    <mi>V</mi>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dpb</mtext>
				    </mrow>
				  </msub>
				  <mo stretchy="false">)</mo>
				  <mspace width="thinmathspace" />
				  <mtext>or</mtext>
				  <mspace width="thinmathspace" />
				  <msub>
				    <mi>V</mi>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dsf</mtext>
				    </mrow>
				  </msub>
				</math>
		&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>db</mtext>
						  </msub>
						</math> = Design strength of bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dsb</mtext>
						  </msub>
						</math> = Design shear capacity of bearing bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dpb</mtext>
						  </msub>
						</math> = Design bearing capacity of bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dsf</mtext>
						  </msub>
						</math> = Design shear capacity of friction grip bolt <br>	<br>

&emsp; <b> <strong> v. Number of bolts <math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>(n)</mi>
						</math> </strong> <br>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
					  <mi>n</mi>
					  <mo>=</mo>
					  <mtext>Ceiling</mtext>
					  <mspace width="thinmathspace" />
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo maxsize="2.047em" minsize="2.047em">[</mo>
					  </mrow>
					  <mfrac>
					    <mtext>Force in flange</mtext>
					    <mtext>Bolt value</mtext>
					  </mfrac>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo maxsize="2.047em" minsize="2.047em">]</mo>
					  </mrow>
					</math>
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step8_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step8-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->condition('uid', $user->uid);
	$form_step8_data = $query->execute();
	if ($form_step8_data)
	{
		if ($step8_data = $form_step8_data->fetchObject())
		{
			$form['step8_field1_fieldset']['step8_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step8_field1_fieldset']['step8_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step8_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step8_field1_fieldset']['step8_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step8_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step8_field1_fieldset\\[step8_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step8_data->id, $step8_data->data_relation);
			$icom = 1;
			$form['step8_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr>Earlier comment<hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step8_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step8_num_comment']))
			{
				$form_state['step8_num_comment'] = 1;
			} //empty($form_state['step8_num_comment'])
			$step8_temp1 = 0;
			for ($step8_i = 0; $step8_i < $form_state['step8_num_comment']; $step8_i++)
			{
				$step8_temp1 = $step8_i;
				$form['step8_field1_fieldset'][$step8_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step8_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step8_field1_fieldset']["step8_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step8_temp1
			);
			$form['step8_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step8_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step8_comment_add_more_callback',
					'wrapper' => 'step8-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step8_num_comment'] > 1)
			{
				$form['step8_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step8_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step8_comment_add_more_callback',
						'wrapper' => 'step8-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step8_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step8_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step8_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step8_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step8_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step8_form_next_submit'
				)
			);
		} //$step8_data = $form_step8_data->fetchObject()
		else
		{
			$form['step8_field1_fieldset']['step8_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step8_field1_fieldset']['step8_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step8_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step8_field1_fieldset']['step8_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step8_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step8_field1_fieldset\\[step8_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step8_num_comment']))
			{
				$form_state['step8_num_comment'] = 1;
			} //empty($form_state['step8_num_comment'])
			$step8_temp1 = 0;
			for ($step8_i = 0; $step8_i < $form_state['step8_num_comment']; $step8_i++)
			{
				$step8_temp1 = $step8_i;
				$form['step8_field1_fieldset'][$step8_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step8_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step8_field1_fieldset']["step8_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step8_temp1
			);
			$form['step8_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step8_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step8_comment_add_more_callback',
					'wrapper' => 'step8-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step8_num_comment'] > 1)
			{
				$form['step8_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step8_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step8_comment_add_more_callback',
						'wrapper' => 'step8-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step8_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step8_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step8_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step8_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step8_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step8_form_next_submit'
				)
			);
		} //$step8_data = $form_step8_data->fetchObject()
	} //$form_step8_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step8_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step8_field1_fieldset']['step8_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->condition('uid', $user->uid);
	$form_step8_data = $query->execute()->fetchObject();
	//var_dump($form_step8_data);die;
	if ($form_step8_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step8_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step8_field1_fieldset']['step8_field1_question1'],
			":question_ok_not_ok" => $v['step8_field1_fieldset']['step8_field1_question_ok'],
			":question_not_ok_comment" => $v['step8_field1_fieldset']['step8_field1_question_not_ok_comment'],
			":data_relation" => "step8"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step8_data->id
		));
		$form_step8_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++)
		{
			if ($v['step8_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step8_data->id,
					":number" => $i + $form_step8_comment_data->max + 1,
					":comment" => $v['step8_field1_fieldset'][$i]["comment"],
					":data_relation" => "step8",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step8_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++
	} //$form_step8_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step8_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step8_field1_fieldset']['step8_field1_question1'],
			":question_ok_not_ok" => $v['step8_field1_fieldset']['step8_field1_question_ok'],
			":question_not_ok_comment" => $v['step8_field1_fieldset']['step8_field1_question_not_ok_comment'],
			":data_relation" => "step8",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++)
		{
			if ($v['step8_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step8_field1_fieldset'][$i]["comment"],
					":data_relation" => "step8",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step8_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step7/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step8_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step8_field1_fieldset']['step8_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->condition('uid', $user->uid);
	$form_step8_data = $query->execute()->fetchObject();
	//var_dump($form_step8_data);die;
	if ($form_step8_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step8_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step8_field1_fieldset']['step8_field1_question1'],
			":question_ok_not_ok" => $v['step8_field1_fieldset']['step8_field1_question_ok'],
			":question_not_ok_comment" => $v['step8_field1_fieldset']['step8_field1_question_not_ok_comment'],
			":data_relation" => "step8"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step8_data->id
		));
		$form_step8_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++)
		{
			if ($v['step8_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step8_data->id,
					":number" => $i + $form_step8_comment_data->max + 1,
					":comment" => $v['step8_field1_fieldset'][$i]["comment"],
					":data_relation" => "step8",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step8_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++
	} //$form_step8_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step8_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step8_field1_fieldset']['step8_field1_question1'],
			":question_ok_not_ok" => $v['step8_field1_fieldset']['step8_field1_question_ok'],
			":question_not_ok_comment" => $v['step8_field1_fieldset']['step8_field1_question_not_ok_comment'],
			":data_relation" => "step8",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++)
		{
			if ($v['step8_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step8_field1_fieldset'][$i]["comment"],
					":data_relation" => "step8",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step8_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step8_field1_fieldset']["step8_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step9/' . $user->uid;
}
/***************************************/
function step8_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step8_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step8_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step8_num_comment'] > 1)
	{
		$form_state['step8_num_comment']--;
	} //$form_state['step8_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step8_comment_add_more_callback($form, &$form_state)
{
	return $form['step8_field1_fieldset'];
}
/***************************************/
/***************************************** step 8 from ends ****************************/
/************************ Step 9 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step9_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('e. Detailing checks > i. Minimum pitch and gauge distance > ii. Maximum pitch and gauge distance > iii. Gauge1 > iv. End and edge distance'));
	$img_path = $base_url . '/' . drupal_get_path("module", "osdag_response_form") . '/images';
	$markup_text = '
	<b> <strong> e. Detailing checks </strong> </b> <br>
	&emsp; <b> <strong>	i. Minimum  pitch and gauge distance </strong> [Reference: Clause 10.2.2 page 73, IS 800 : 2007] <br>
				 <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <mrow class="MJX-TeXAtom-ORD">
				    <mi>p</mi>
				  </mrow>
				  <mo>&#x2265;<!-- ≥ --></mo>
				  <mrow class="MJX-TeXAtom-ORD">
				    <mn>2.5</mn>
				    <mspace width="thinmathspace" />
				    <mi>d</mi>
				  </mrow>
				</math> 
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <mrow class="MJX-TeXAtom-ORD">
				    <mi>g</mi>
				  </mrow>
				  <mo>&#x2265;<!-- ≥ --></mo>
				  <mrow class="MJX-TeXAtom-ORD">
				    <mn>2.5</mn>
				    <mspace width="thinmathspace" />
				    <mi>d</mi>
				  </mrow><br> 
				</math>

	&emsp; <b> <strong>	ii. Maximum pitch and gauge distance </strong> </b>[Reference: Clause 10.2.3.1 page 74, IS 800 : 2007] <br>	
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <mrow class="MJX-TeXAtom-ORD">
				    <mi>p</mi>
				  </mrow>
				  <mo>&#x2264;<!-- ≤ --></mo>
				  <mtext>min</mtext>
				  <mspace width="thinmathspace" />
				  <mo stretchy="false">(</mo>
				  <mrow class="MJX-TeXAtom-ORD">
				    <mn>32</mn>
				    <mspace width="thinmathspace" />
				    <mi>t</mi>
				    <mo>,</mo>
				    <mn>300</mn>
				  </mrow>
				  <mo stretchy="false">)</mo>
				</math> 
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <mrow class="MJX-TeXAtom-ORD">
				    <mi>g</mi>
				  </mrow>
				  <mo>&#x2264;<!-- ≤ --></mo>
				  <mtext>min</mtext>
				  <mspace width="thinmathspace" />
				  <mo stretchy="false">(</mo>
				  <mrow class="MJX-TeXAtom-ORD">
				    <mn>32</mn>
				    <mspace width="thinmathspace" />
				    <mi>t</mi>
				    <mo>,</mo>
				    <mn>300</mn>
				  </mrow>
				  <mo stretchy="false">)</mo>
				</math> 


					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>p</mi>
						</math> = Pitch distance <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>g</mi>
						</math> = Gauge ditance <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>d</mi>
						</math> = Nominal bolt diameter <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>t</mi>
						</math> = Thickness of the thinner plate <br>
							&emsp;&emsp;&emsp; <strong> The above step i. and ii. are same as implemented in the shear connection modules (already reviewed). </strong>
	<br> <br>
			&emsp; <b> <strong>	iii. Gauge1 </strong> </b>[Reference: Steel Designers Manual -SCI - 6th Edition (2003), page 734 ] <br>		
				&emsp;&emsp;&emsp;	Gauge1 (also called cross centre distance, g1) values will be subjected to the following limits (in mm). <br> 
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mn>90</mn>
  <mo>&lt;</mo>
  <mrow class="MJX-TeXAtom-ORD">
    <mi>g</mi>
    <mn>1</mn>
  </mrow>
  <mo>&lt;</mo>
  <mn>140</mn>
</math> &emsp;&emsp;&emsp; <strong> Web splice plate has a gauge distance equal to cross center distance. </strong>				

<br> <br>
			&emsp; <b> <strong>	iv. Edge and end distance </strong> </b>[Reference: Clause 10.2.4 page 74, IS 800 : 2007] <br>
		&emsp;&emsp;&emsp;	The minimum edge and end distances from the centre of any hole to the nearest edge of the column/end plate shall not be less than 1.7 times the hole diameter in case of sheared or hand-flame cut edges; and 1.5 times the hole diameter in case of rolled, machine-flame cut, sawn and planed edges. <br>
				
						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>1</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>

						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>2</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>

						&emsp;&emsp;&emsp; The maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part should not exceed 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mn>12</mn>
		  <mi>t</mi>
		  <mi>&#x03F5;<!-- ϵ --></mi>
		</math>
	, where
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>&#x03F5;<!-- ϵ --></mi>
		  <mo>=</mo>
		  <msqrt>
			<mn>250</mn>
			<mrow class="MJX-TeXAtom-ORD">
			  <mo>/</mo>
			</mrow>
			<msub>
			  <mi>f</mi>
			  <mi>y</mi>
			</msub>
		  </msqrt>
		</math>
	and 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>t</mi>
		</math>
	is the thickness of the thinner component.  <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
					<mi>e</mi>
					<mn>2</mn>
				  </msub>
				  <mo>&#x2264;</mo>
				  <mn>12</mn>
				  <mi>t</mi>
				  <mi>&#x03F5;<!-- ϵ --></mi>
				</math>
			
		&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
		Where, <br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>1</mn>
			  </msub>
			</math>
			= End distance <br>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>2</mn>
			  </msub>
			</math>
			= Edge distance <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>d</mi>
				<mn>h</mn>
			  </msub>
			</math> 
			= Diameter of bolt hole <br>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>f</mi>
				<mn>y</mn>
			  </msub>
			</math>
			= Characteristic yield stress <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
				<mi>t</mi>
			</math> 
			= thickness of the thinner component 
			<br>
			<br>
			&emsp;&emsp;&emsp; <strong> The above step iv. is same as implemented in the shear connection modules (already reviewed). </strong> <br><br>

			
			&emsp;&emsp;&emsp;
			<strong> Note: </strong> Where the members are exposed to corrosive influences, the maximum edge distance shall not exceed 40 mm plus 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mn>4</mn>
					<mi>t</mi>
			</math> 
			, where 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mi>t</mi>
			</math> 
			is the thickness of thinner connected plate.
			
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step9_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step9-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step9_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step9_feedback');
	$query->condition('uid', $user->uid);
	$form_step9_data = $query->execute();
	if ($form_step9_data)
	{
		if ($step9_data = $form_step9_data->fetchObject())
		{
			$form['step9_field1_fieldset']['step9_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step9_field1_fieldset']['step9_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step9_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step9_field1_fieldset']['step9_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step9_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step9_field1_fieldset\\[step9_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step9_data->id, $step9_data->data_relation);
			$icom = 1;
			$form['step9_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr><strong>Earlier comment</strong><hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step9_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step9_num_comment']))
			{
				$form_state['step9_num_comment'] = 1;
			} //empty($form_state['step9_num_comment'])
			$step9_temp1 = 0;
			for ($step9_i = 0; $step9_i < $form_state['step9_num_comment']; $step9_i++)
			{
				$step9_temp1 = $step9_i;
				$form['step9_field1_fieldset'][$step9_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step9_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step9_field1_fieldset']["step9_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step9_temp1
			);
			$form['step9_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step9_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step9_comment_add_more_callback',
					'wrapper' => 'step9-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step9_num_comment'] > 1)
			{
				$form['step9_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step9_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step9_comment_add_more_callback',
						'wrapper' => 'step9-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step9_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step9_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step9_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step9_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step9_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step9_form_next_submit'
				)
			);
		} //$step9_data = $form_step9_data->fetchObject()
		else
		{
			$form['step9_field1_fieldset']['step9_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step9_field1_fieldset']['step9_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step9_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step9_field1_fieldset']['step9_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step9_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step9_field1_fieldset\\[step9_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step9_num_comment']))
			{
				$form_state['step9_num_comment'] = 1;
			} //empty($form_state['step9_num_comment'])
			$step9_temp1 = 0;
			for ($step9_i = 0; $step9_i < $form_state['step9_num_comment']; $step9_i++)
			{
				$step9_temp1 = $step9_i;
				$form['step9_field1_fieldset'][$step9_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step9_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step9_field1_fieldset']["step9_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step9_temp1
			);
			$form['step9_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step9_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step9_comment_add_more_callback',
					'wrapper' => 'step9-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step9_num_comment'] > 1)
			{
				$form['step9_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step9_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step9_comment_add_more_callback',
						'wrapper' => 'step9-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step9_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step9_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step9_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step9_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step9_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step9_form_next_submit'
				)
			);
		} //$step9_data = $form_step9_data->fetchObject()
	} //$form_step9_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step9_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step9_field1_fieldset']['step9_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step9_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step9_feedback');
	$query->condition('uid', $user->uid);
	$form_step9_data = $query->execute()->fetchObject();
	//var_dump($form_step9_data);die;
	if ($form_step9_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step9_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step9_field1_fieldset']['step9_field1_question1'],
			":question_ok_not_ok" => $v['step9_field1_fieldset']['step9_field1_question_ok'],
			":question_not_ok_comment" => $v['step9_field1_fieldset']['step9_field1_question_not_ok_comment'],
			":data_relation" => "step9"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step9_data->id
		));
		$form_step9_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++)
		{
			if ($v['step9_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step9_data->id,
					":number" => $i + $form_step9_comment_data->max + 1,
					":comment" => $v['step9_field1_fieldset'][$i]["comment"],
					":data_relation" => "step9",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step9_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++
	} //$form_step9_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step9_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step9_field1_fieldset']['step9_field1_question1'],
			":question_ok_not_ok" => $v['step9_field1_fieldset']['step9_field1_question_ok'],
			":question_not_ok_comment" => $v['step9_field1_fieldset']['step9_field1_question_not_ok_comment'],
			":data_relation" => "step9",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++)
		{
			if ($v['step9_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step9_field1_fieldset'][$i]["comment"],
					":data_relation" => "step9",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step9_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step8/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step9_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step9_field1_fieldset']['step9_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step9_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step9_feedback');
	$query->condition('uid', $user->uid);
	$form_step9_data = $query->execute()->fetchObject();
	//var_dump($form_step9_data);die;
	if ($form_step9_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step9_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step9_field1_fieldset']['step9_field1_question1'],
			":question_ok_not_ok" => $v['step9_field1_fieldset']['step9_field1_question_ok'],
			":question_not_ok_comment" => $v['step9_field1_fieldset']['step9_field1_question_not_ok_comment'],
			":data_relation" => "step9"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step9_data->id
		));
		$form_step9_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++)
		{
			if ($v['step9_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step9_data->id,
					":number" => $i + $form_step9_comment_data->max + 1,
					":comment" => $v['step9_field1_fieldset'][$i]["comment"],
					":data_relation" => "step9",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step9_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++
	} //$form_step9_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step9_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step9_field1_fieldset']['step9_field1_question1'],
			":question_ok_not_ok" => $v['step9_field1_fieldset']['step9_field1_question_ok'],
			":question_not_ok_comment" => $v['step9_field1_fieldset']['step9_field1_question_not_ok_comment'],
			":data_relation" => "step9",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++)
		{
			if ($v['step9_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step9_field1_fieldset'][$i]["comment"],
					":data_relation" => "step9",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step9_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step9_field1_fieldset']["step9_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step10/' . $user->uid;
}
/***************************************/
function step9_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step9_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step9_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step9_num_comment'] > 1)
	{
		$form_state['step9_num_comment']--;
	} //$form_state['step9_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step9_comment_add_more_callback($form, &$form_state)
{
	return $form['step9_field1_fieldset'];
}
/***************************************/
/***************************************** step 9 from ends ****************************/
/************************ Step 10 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step10_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('e. Detailing checks > v. Flange splice plate vi. Web splice plate'));
	$img_path = $base_url . '/' . drupal_get_path("module", "osdag_response_form") . '/images';
	$markup_text = '
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;				
				<img src="' . $img_path . '/ddcl_BB_splice_cover_plate_bolted_1.png" width="70%" height="70%" align="middle" />
				<br><br>
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
				Figure: Essential detailing requirements for a splice (external flange cover plates) <br> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;[Reference: Steel Designer`s Manual - SCI - 6th edition, page 754]
				<hr>

				<b> <strong> e. Detailing checks </strong> </b> <br>
				&emsp; <b> <strong> v. Flange splice plate </strong> </b> <br>
				&emsp;&emsp;
						Referring to the above figure: <br>
					&emsp;&emsp;&emsp;	
							a. Height of flange splice plate > <math xmlns="http://www.w3.org/1998/Math/MathML">
								  <msub>
								    <mi>L</mi>
								    <mrow class="MJX-TeXAtom-ORD">
								      <mtext>tp</mtext>
								    </mrow>
								  </msub>
								  <mo>+</mo>
								  <mtext>Gap</mtext>
								  <mo>+</mo>
								  <msub>
								    <mi>L</mi>
								    <mrow class="MJX-TeXAtom-ORD">
								      <mtext>tp</mtext>
								    </mrow>
								  </msub>
								</math>  (Note: <math xmlns="http://www.w3.org/1998/Math/MathML">
							  <msub>
								    <mi>L</mi>
								      <mtext>tp</mtext>
								  </msub>
							</math> > <math xmlns="http://www.w3.org/1998/Math/MathML">
								    <mi>B</mi>
							</math> and 225mm)<br>
						&emsp;&emsp;&emsp;	b. 	Width of flange splice plate = B - 1/2 inch on each side of flange or B (for splicing beams or columns of same size) [Reference: 30 good rules for connection design, AISC] <br>
						
						&emsp;&emsp;&emsp;	c. Minimum thickness of flange splice plate (<math xmlns="http://www.w3.org/1998/Math/MathML">
								  <msub>
								    <mi>t</mi>
								    <mrow class="MJX-TeXAtom-ORD">
								      <mtext>p, min</mtext>
								    </mrow>
								  </msub>
							</math>) = half the flange thickness and 10 mm <br>

							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
							where, <br>

							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <math xmlns="http://www.w3.org/1998/Math/MathML">
								    <mi>B</mi>
							</math> = Width of flange <br>
<br>
				&emsp; <b> <strong> vi. Web splice plate </strong> </b> <br>
				&emsp;&emsp;
						Referring to the above figure: <br>
						&emsp;&emsp;&emsp; a. Minimum height of web splice plate <math xmlns="http://www.w3.org/1998/Math/MathML" >
							  <mo stretchy="false">(</mo>
							  <msub>
							    <mi>h</mi>
							    <mrow class="MJX-TeXAtom-ORD">
							      <mtext>p, min</mtext>
							    </mrow>
							  </msub>
							  <mo stretchy="false">)</mo>
							  <mo>=</mo>
							  <mn>0.5</mn>
							  <mi>D</mi>
							</math> <br>


						&emsp;&emsp;&emsp; b. Maximum height of web splice plate [Reference: Bolted field splices for steel bridge flexural members AISC - overview and design example, section 2.2.1.3 page 14] <br>
						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mi>h</mi>
						    </mrow>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>p, max</mtext>
						    </mrow>
						  </msub>
						  <mo>=</mo>
						  <mrow class="MJX-TeXAtom-ORD">
						    <mi>D</mi>
						  </mrow>
						  <mo>&#x2212;<!-- − --></mo>
						  <mn>2</mn>
						  <mspace width="thinmathspace" />
						  <msub>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mi>t</mi>
						    </mrow>
						    <mtext>f</mtext>
						  </msub>
						  <mo>&#x2212;<!-- − --></mo>
						  <mn>2</mn>
						  <mspace width="thinmathspace" />
						  <msub>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mi>r</mi>
						    </mrow>
						    <mn>1</mn>
						  </msub>
						  <mo>&#x2212;<!-- − --></mo>
						  <mn>2</mn>
						  <mspace width="thinmathspace" />
						  <mi>&#x03F5;<!-- ϵ --></mi>
						</math> 

						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
							where, <br>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <math xmlns="http://www.w3.org/1998/Math/MathML">
							  <mi>D</mi>
							</math> = Overall depth of supported beam <br>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <math xmlns="http://www.w3.org/1998/Math/MathML">
							    <mn>2</mn>
								  <mspace width="thinmathspace" />
								  <msub>
								    <mi>t</mi>
								    <mrow class="MJX-TeXAtom-ORD">
								      <mtext>f</mtext>
								    </mrow>
								  </msub>
							</math> = Thickness of flange <br>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <math xmlns="http://www.w3.org/1998/Math/MathML">
							    <mn>2</mn>
								  <mspace width="thinmathspace" />
								  <msub>
								    <mi>r</mi>
								    <mn>1</mn>
								  </msub>
							</math> = Root radius of the beam section <br>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; <math xmlns="http://www.w3.org/1998/Math/MathML">
							    <mi>&#x03F5;<!-- ϵ --></mi>
							</math> = Assumed gap or clearance (5mm) <br>

						&emsp;&emsp;&emsp;	<strong> Note: </strong>		Webs are to be spliced symmetrically by plates on each side. The splice plates are to extend as near as practical for full depth between flanges without impinging on bolt assembly clearances. <br>


			
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step10_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step10-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step10_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step10_feedback');
	$query->condition('uid', $user->uid);
	$form_step10_data = $query->execute();
	if ($form_step10_data)
	{
		if ($step10_data = $form_step10_data->fetchObject())
		{
			$form['step10_field1_fieldset']['step10_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step10_field1_fieldset']['step10_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step10_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step10_field1_fieldset']['step10_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step10_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step10_field1_fieldset\\[step10_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step10_data->id, $step10_data->data_relation);
			$icom = 1;
			$form['step10_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr><strong>Earlier comment</strong><hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step10_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step10_num_comment']))
			{
				$form_state['step10_num_comment'] = 1;
			} //empty($form_state['step10_num_comment'])
			$step10_temp1 = 0;
			for ($step10_i = 0; $step10_i < $form_state['step10_num_comment']; $step10_i++)
			{
				$step10_temp1 = $step10_i;
				$form['step10_field1_fieldset'][$step10_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step10_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step10_field1_fieldset']["step10_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step10_temp1
			);
			$form['step10_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step10_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step10_comment_add_more_callback',
					'wrapper' => 'step10-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step10_num_comment'] > 1)
			{
				$form['step10_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step10_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step10_comment_add_more_callback',
						'wrapper' => 'step10-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step10_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step10_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step10_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step10_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step10_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step10_form_next_submit'
				)
			);
		} //$step10_data = $form_step10_data->fetchObject()
		else
		{
			$form['step10_field1_fieldset']['step10_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step10_field1_fieldset']['step10_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step2_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step10_field1_fieldset']['step10_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step2_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step10_field1_fieldset\\[step10_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step10_num_comment']))
			{
				$form_state['step10_num_comment'] = 1;
			} //empty($form_state['step10_num_comment'])
			$step10_temp1 = 0;
			for ($step10_i = 0; $step10_i < $form_state['step10_num_comment']; $step10_i++)
			{
				$step10_temp1 = $step10_i;
				$form['step10_field1_fieldset'][$step10_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step10_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step10_field1_fieldset']["step10_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step10_temp1
			);
			$form['step10_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step10_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step10_comment_add_more_callback',
					'wrapper' => 'step10-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step10_num_comment'] > 1)
			{
				$form['step10_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step10_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step10_comment_add_more_callback',
						'wrapper' => 'step10-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step10_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step10_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step10_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step10_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step10_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step10_form_next_submit'
				)
			);
		} //$step10_data = $form_step10_data->fetchObject()
	} //$form_step10_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step10_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step10_field1_fieldset']['step10_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step10_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step10_feedback');
	$query->condition('uid', $user->uid);
	$form_step10_data = $query->execute()->fetchObject();
	//var_dump($form_step10_data);die;
	if ($form_step10_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step10_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step10_field1_fieldset']['step10_field1_question1'],
			":question_ok_not_ok" => $v['step10_field1_fieldset']['step10_field1_question_ok'],
			":question_not_ok_comment" => $v['step10_field1_fieldset']['step10_field1_question_not_ok_comment'],
			":data_relation" => "step10"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step10_data->id
		));
		$form_step10_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++)
		{
			if ($v['step10_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step10_data->id,
					":number" => $i + $form_step10_comment_data->max + 1,
					":comment" => $v['step10_field1_fieldset'][$i]["comment"],
					":data_relation" => "step10",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step10_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++
	} //$form_step10_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step10_feedback} (uid, question1,  question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step10_field1_fieldset']['step10_field1_question1'],
			":question_ok_not_ok" => $v['step10_field1_fieldset']['step10_field1_question_ok'],
			":question_not_ok_comment" => $v['step10_field1_fieldset']['step10_field1_question_not_ok_comment'],
			":data_relation" => "step10",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++)
		{
			if ($v['step10_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step10_field1_fieldset'][$i]["comment"],
					":data_relation" => "step10",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step10_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step9/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step10_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step10_field1_fieldset']['step10_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step10_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step10_feedback');
	$query->condition('uid', $user->uid);
	$form_step10_data = $query->execute()->fetchObject();
	//var_dump($form_step10_data);die;
	if ($form_step10_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step10_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step10_field1_fieldset']['step10_field1_question1'],
			":question_ok_not_ok" => $v['step10_field1_fieldset']['step10_field1_question_ok'],
			":question_not_ok_comment" => $v['step10_field1_fieldset']['step10_field1_question_not_ok_comment'],
			":data_relation" => "step10"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step10_data->id
		));
		$form_step10_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++)
		{
			if ($v['step10_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step10_data->id,
					":number" => $i + $form_step10_comment_data->max + 1,
					":comment" => $v['step10_field1_fieldset'][$i]["comment"],
					":data_relation" => "step10",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step10_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++
	} //$form_step10_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step10_feedback} (uid, question1,  question_ok_not_ok,question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step10_field1_fieldset']['step10_field1_question1'],
			":question_ok_not_ok" => $v['step10_field1_fieldset']['step10_field1_question_ok'],
			":question_not_ok_comment" => $v['step10_field1_fieldset']['step10_field1_question_not_ok_comment'],
			":data_relation" => "step10",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++)
		{
			if ($v['step10_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step10_field1_fieldset'][$i]["comment"],
					":data_relation" => "step10",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step10_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step10_field1_fieldset']["step10_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step11/' . $user->uid;
}
/***************************************/
function step10_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step10_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step10_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step10_num_comment'] > 1)
	{
		$form_state['step10_num_comment']--;
	} //$form_state['step10_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step10_comment_add_more_callback($form, &$form_state)
{
	return $form['step10_field1_fieldset'];
}
/***************************************/
/***************************************** step 10 from ends ****************************/
/************************ Step 11 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step11_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('f. Thickness of flange splice plate'));
	$markup_text = '
	
	<b> <strong> f. Thickness of flange splice plate </strong> [Reference: N. Subramanian (Page 428), M.L. Gambhir (Page 10.84)] </b> <br> 

			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
		  <mrow class="MJX-TeXAtom-ORD">
		    <mi>t</mi>
		  </mrow>
		  <mo>=</mo>
		  <mfrac>
		    <mtext>Force in flange</mtext>
		    <mrow>
		      <mo stretchy="false">(</mo>
		      <msub>
		        <mrow class="MJX-TeXAtom-ORD">
		          <mi>b</mi>
		        </mrow>
		        <mtext>f</mtext>
		      </msub>
		      <mo stretchy="false">)</mo>
		      <mrow class="MJX-TeXAtom-ORD">
		        <mo stretchy="false">(</mo>
		        <msub>
		          <mrow class="MJX-TeXAtom-ORD">
		            <mi>f</mi>
		          </mrow>
		          <mtext>y</mtext>
		        </msub>
		      </mrow>
		      <mrow class="MJX-TeXAtom-ORD">
		        <mo>/</mo>
		      </mrow>
		      <mrow class="MJX-TeXAtom-ORD">
		        <msub>
		          <mi>&#x03B3;<!-- γ --></mi>
		          <mrow class="MJX-TeXAtom-ORD">
		            <mtext>m0</mtext>
		          </mrow>
		        </msub>
		      </mrow>
		      <mo stretchy="false">)</mo>
		    </mrow>
		  </mfrac>
		  <mo>&gt;</mo>
		  <msub>
		    <mi>t</mi>
		    <mrow class="MJX-TeXAtom-ORD">
		      <mtext>p, min</mtext>
		    </mrow>
		  </msub>
		</math>

		&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>t</mi>
						</math> =  Thickness of flange splice plate <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>b</mi>
						    <mtext>f</mtext>
						  </msub>
						</math> = Width of flange <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m0</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor against yield stress and buckling <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>t</mi>
						    <mtext>p, min</mtext>
						  </msub>
						</math> = Minimum thickness of flange splice plate <br>
			
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step11_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step11-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step11_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step11_feedback');
	$query->condition('uid', $user->uid);
	$form_step11_data = $query->execute();
	if ($form_step11_data)
	{
		if ($step11_data = $form_step11_data->fetchObject())
		{
			$form['step11_field1_fieldset']['step11_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step11_field1_fieldset']['step11_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step11_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step11_field1_fieldset']['step11_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step11_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step11_field1_fieldset\\[step11_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step11_data->id, $step11_data->data_relation);
			$icom = 1;
			$form['step11_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>' 
			); 
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step11_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step11_num_comment']))
			{
				$form_state['step11_num_comment'] = 1;
			} //empty($form_state['step11_num_comment'])
			$step11_temp1 = 0;
			for ($step11_i = 0; $step11_i < $form_state['step11_num_comment']; $step11_i++)
			{
				$step11_temp1 = $step11_i;
				$form['step11_field1_fieldset'][$step11_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step11_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step11_field1_fieldset']["step11_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step11_temp1
			);
			$form['step11_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step11_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step11_comment_add_more_callback',
					'wrapper' => 'step11-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step11_num_comment'] > 1)
			{
				$form['step11_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step11_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step11_comment_add_more_callback',
						'wrapper' => 'step11-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step11_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step11_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step11_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step11_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step11_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step11_form_next_submit'
				)
			);
		} //$step11_data = $form_step11_data->fetchObject()
		else
		{
			$form['step11_field1_fieldset']['step11_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step11_field1_fieldset']['step11_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step11_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step11_field1_fieldset']['step11_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step2_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step11_field1_fieldset\\[step11_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step11_num_comment']))
			{
				$form_state['step11_num_comment'] = 1;
			} //empty($form_state['step11_num_comment'])
			$step11_temp1 = 0;
			for ($step11_i = 0; $step11_i < $form_state['step11_num_comment']; $step11_i++)
			{
				$step11_temp1 = $step11_i;
				$form['step11_field1_fieldset'][$step11_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step11_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step11_field1_fieldset']["step11_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step11_temp1
			);
			$form['step11_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step11_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step11_comment_add_more_callback',
					'wrapper' => 'step11-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step11_num_comment'] > 1)
			{
				$form['step11_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step11_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step11_comment_add_more_callback',
						'wrapper' => 'step11-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step11_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step11_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step11_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step11_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step11_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step11_form_next_submit'
				)
			);
		} //$step11_data = $form_step11_data->fetchObject()
	} //$form_step11_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step11_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step11_field1_fieldset']['step11_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step11_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step11_feedback');
	$query->condition('uid', $user->uid);
	$form_step11_data = $query->execute()->fetchObject();
	//var_dump($form_step11_data);die;
	if ($form_step11_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step11_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step11_field1_fieldset']['step11_field1_question1'],
			":question_ok_not_ok" => $v['step11_field1_fieldset']['step11_field1_question_ok'],
			":question_not_ok_comment" => $v['step11_field1_fieldset']['step11_field1_question_not_ok_comment'],
			":data_relation" => "step11"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step11_data->id
		));
		$form_step11_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++)
		{
			if ($v['step11_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step11_data->id,
					":number" => $i + $form_step11_comment_data->max + 1,
					":comment" => $v['step11_field1_fieldset'][$i]["comment"],
					":data_relation" => "step11",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step11_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++
	} //$form_step11_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step11_feedback} (uid, question1,question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step11_field1_fieldset']['step11_field1_question1'],
			":question_ok_not_ok" => $v['step11_field1_fieldset']['step11_field1_question_ok'],
			":question_not_ok_comment" => $v['step11_field1_fieldset']['step11_field1_question_not_ok_comment'],
			":data_relation" => "step11",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++)
		{
			if ($v['step11_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step11_field1_fieldset'][$i]["comment"],
					":data_relation" => "step11",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step11_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step10/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step11_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step11_field1_fieldset']['step11_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step11_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step11_feedback');
	$query->condition('uid', $user->uid);
	$form_step11_data = $query->execute()->fetchObject();
	//var_dump($form_step11_data);die;
	if ($form_step11_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step11_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step11_field1_fieldset']['step11_field1_question1'],
			":question_ok_not_ok" => $v['step11_field1_fieldset']['step11_field1_question_ok'],
			":question_not_ok_comment" => $v['step11_field1_fieldset']['step11_field1_question_not_ok_comment'],
			":data_relation" => "step11"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step11_data->id
		));
		$form_step11_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++)
		{
			if ($v['step11_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step11_data->id,
					":number" => $i + $form_step11_comment_data->max + 1,
					":comment" => $v['step11_field1_fieldset'][$i]["comment"],
					":data_relation" => "step11",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step11_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++
	} //$form_step11_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step11_feedback} (uid, question1,question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step11_field1_fieldset']['step11_field1_question1'],
			":question_ok_not_ok" => $v['step11_field1_fieldset']['step11_field1_question_ok'],
			":question_not_ok_comment" => $v['step11_field1_fieldset']['step11_field1_question_not_ok_comment'],
			":data_relation" => "step11",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++)
		{
			if ($v['step11_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step11_field1_fieldset'][$i]["comment"],
					":data_relation" => "step11",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step11_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step11_field1_fieldset']["step11_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step12/' . $user->uid;
}
/***************************************/
function step11_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step11_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step11_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step11_num_comment'] > 1)
	{
		$form_state['step11_num_comment']--;
	} //$form_state['step11_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step11_comment_add_more_callback($form, &$form_state)
{
	return $form['step11_field1_fieldset'];
}
/***************************************/
/***************************************** step 11 from ends ****************************/
/************************ Step 12 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step12_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of flange splice > d. Bolt > vi. Re-Check for bolt value (long joints)'));
	$markup_text = '
	
	<b> <strong> d. Bolt </strong> </b> <br>
	&emsp; <b> <strong> vi. Re-Check for bolt value (long joints) </strong> [Reference: Clause 10.3.3.1 page 75, IS 800 : 2007] </b> <br>
	&emsp;&emsp; Shear capacity (bearing and HSFG bolt) of the bolts are evaluated again considering long joint provision. <br>
	&emsp;&emsp;When the length of joint, <math xmlns="http://www.w3.org/1998/Math/MathML" >
  <msub>
    <mi>l</mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>j</mtext>
    </mrow>
  </msub>
</math>  of a splice or end connection in compression or tension element containing more than two bolts (that is distance between the first and last rows of bolts in the joint, measured in the direction of load transfer) exceeds 15d in the direction of load, the nominal shear capacity <math xmlns="http://www.w3.org/1998/Math/MathML" >
  <msub>
    <mi>V</mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>db</mtext>
    </mrow>
  </msub>
</math> shall be reduced by the factor <math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub>
    <mi>&#x03B2;<!-- β --></mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>lj</mtext>
    </mrow>
  </msub>
</math>. <br>

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <msub>
    <mi>&#x03B2;<!-- β --></mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>lj</mtext>
    </mrow>
  </msub>
  <mo>=</mo>
  <mn>1.075</mn>
  <mo>&#x2212;<!-- − --></mo>
  <mfrac>
    <msub>
      <mrow class="MJX-TeXAtom-ORD">
        <mi>l</mi>
      </mrow>
      <mtext>j</mtext>
    </msub>
    <mrow class="MJX-TeXAtom-ORD">
      <mn>200</mn>
      <mspace width="thinmathspace" />
      <mi>d</mi>
    </mrow>
  </mfrac>
  <mspace width="thinmathspace" />
  <mspace width="thinmathspace" />
  <mspace width="thinmathspace" />
  <mtext>But</mtext>
  <mo>,</mo>
  <mn>0.75</mn>
  <mo>&#x2264;<!-- ≤ --></mo>
  <msub>
    <mi>&#x03B2;<!-- β --></mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>lj</mtext>
    </mrow>
  </msub>
  <mo>&#x2264;<!-- ≤ --></mo>
  <mn>1.0</mn>
</math>

	<hr>';
	// All the real form fields.
	$form = array();
	$form['step12_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step12-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step12_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step12_feedback');
	$query->condition('uid', $user->uid);
	$form_step12_data = $query->execute();
	if ($form_step12_data)
	{
		if ($step12_data = $form_step12_data->fetchObject())
		{
			$form['step12_field1_fieldset']['step12_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step12_field1_fieldset']['step12_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step12_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step12_field1_fieldset']['step12_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step12_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step12_field1_fieldset\\[step12_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step12_data->id, $step12_data->data_relation);
			$icom = 1;
			$form['step12_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => '<hr><strong>Earlier comment<strong><hr><br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step12_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step12_num_comment']))
			{
				$form_state['step12_num_comment'] = 1;
			} //empty($form_state['step12_num_comment'])
			$step12_temp1 = 0;
			for ($step12_i = 0; $step12_i < $form_state['step12_num_comment']; $step12_i++)
			{
				$step12_temp1 = $step12_i;
				$form['step12_field1_fieldset'][$step12_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step12_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step12_field1_fieldset']["step12_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step12_temp1
			);
			$form['step12_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step12_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step12_comment_add_more_callback',
					'wrapper' => 'step12-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step12_num_comment'] > 1)
			{
				$form['step12_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step12_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step12_comment_add_more_callback',
						'wrapper' => 'step12-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step12_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step12_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step12_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step12_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step12_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step12_form_next_submit'
				)
			);
		} //$step12_data = $form_step12_data->fetchObject()
		else
		{
			$form['step12_field1_fieldset']['step12_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step12_field1_fieldset']['step12_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step2_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step12_field1_fieldset']['step12_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step2_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step12_field1_fieldset\\[step12_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step12_num_comment']))
			{
				$form_state['step12_num_comment'] = 1;
			} //empty($form_state['step12_num_comment'])
			$step12_temp1 = 0;
			for ($step12_i = 0; $step12_i < $form_state['step12_num_comment']; $step12_i++)
			{
				$step12_temp1 = $step12_i;
				$form['step12_field1_fieldset'][$step12_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step12_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step12_field1_fieldset']["step12_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step12_temp1
			);
			$form['step12_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step12_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step12_comment_add_more_callback',
					'wrapper' => 'step12-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step12_num_comment'] > 1)
			{
				$form['step12_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step12_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step12_comment_add_more_callback',
						'wrapper' => 'step12-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step12_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step12_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step12_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step12_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step12_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step12_form_next_submit'
				)
			);
		} //$step12_data = $form_step12_data->fetchObject()
	} //$form_step12_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step12_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step12_field1_fieldset']['step12_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step12_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step12_feedback');
	$query->condition('uid', $user->uid);
	$form_step12_data = $query->execute()->fetchObject();
	//var_dump($form_step12_data);die;
	if ($form_step12_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step12_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step12_field1_fieldset']['step12_field1_question1'],
			":question_ok_not_ok" => $v['step12_field1_fieldset']['step12_field1_question_ok'],
			":question_not_ok_comment" => $v['step12_field1_fieldset']['step12_field1_question_not_ok_comment'],
			":data_relation" => "step12"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step12_data->id
		));
		$form_step12_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++)
		{
			if ($v['step12_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step12_data->id,
					":number" => $i + $form_step12_comment_data->max + 1,
					":comment" => $v['step12_field1_fieldset'][$i]["comment"],
					":data_relation" => "step12",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step12_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++
	} //$form_step12_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step12_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step12_field1_fieldset']['step12_field1_question1'],
			":question_ok_not_ok" => $v['step12_field1_fieldset']['step12_field1_question_ok'],
			":question_not_ok_comment" => $v['step12_field1_fieldset']['step12_field1_question_not_ok_comment'],
			":data_relation" => "step12",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++)
		{
			if ($v['step12_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step12_field1_fieldset'][$i]["comment"],
					":data_relation" => "step12",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step12_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step11/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step12_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step12_field1_fieldset']['step12_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step12_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step12_feedback');
	$query->condition('uid', $user->uid);
	$form_step12_data = $query->execute()->fetchObject();
	//var_dump($form_step12_data);die;
	if ($form_step12_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step12_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step12_field1_fieldset']['step12_field1_question1'],
			":question_ok_not_ok" => $v['step12_field1_fieldset']['step12_field1_question_ok'],
			":question_not_ok_comment" => $v['step12_field1_fieldset']['step12_field1_question_not_ok_comment'],
			":data_relation" => "step12"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step12_data->id
		));
		$form_step12_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++)
		{
			if ($v['step12_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step12_data->id,
					":number" => $i + $form_step12_comment_data->max + 1,
					":comment" => $v['step12_field1_fieldset'][$i]["comment"],
					":data_relation" => "step12",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step12_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++
	} //$form_step12_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step12_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok, :question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step12_field1_fieldset']['step12_field1_question1'],
			":question_ok_not_ok" => $v['step12_field1_fieldset']['step12_field1_question_ok'],
			":question_not_ok_comment" => $v['step12_field1_fieldset']['step12_field1_question_not_ok_comment'],
			":data_relation" => "step12",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++)
		{
			if ($v['step12_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step12_field1_fieldset'][$i]["comment"],
					":data_relation" => "step12",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step12_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step12_field1_fieldset']["step12_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step13/' . $user->uid;
}
/***************************************/
function step12_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step12_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step12_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step12_num_comment'] > 1)
	{
		$form_state['step12_num_comment']--;
	} //$form_state['step12_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step12_comment_add_more_callback($form, &$form_state)
{
	return $form['step12_field1_fieldset'];
}
/***************************************/
/***************************************** step 12 from ends ****************************/
/************************ Step 13 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step13_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	$img_path = $base_url . '/' . drupal_get_path("module", "osdag_response_form") . '/images';
	drupal_set_title(t('Design of flange splice > g. Capacity of flange'));	
	$markup_text = '
	<b> <strong> g. Capacity of flange </strong> [Reference: N. Subramanian (Page 428), M.L. Gambhir (Page 10.84)]</b> <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <mtext>Net or effective area of flange</mtext>
				  <mo>=</mo>
				  <mo stretchy="false">(</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>b</mi>
				    </mrow>
				    <mtext>f</mtext>
				  </msub>
				  <mo>&#x2212;<!-- − --></mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>n</mi>
				      <mspace width="thinmathspace" />
				      <mi>d</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mspace width="thinmathspace" />
				      <mn>0</mn>
				    </mrow>
				  </msub>
				  <mo stretchy="false">)</mo>
				  <mspace width="thinmathspace" />
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>t</mi>
				    </mrow>
				    <mtext>f</mtext>
				  </msub>
				</math> <br>

			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
			  <mtext>Capacity of the flange</mtext>
			  <mo>=</mo>
			  <mfrac>
			    <mrow>
			      <mtext>Net or effective area of the flange</mtext>
			      <mo>&#x00D7;<!-- × --></mo>
			      <msub>
			        <mrow class="MJX-TeXAtom-ORD">
			          <mi>f</mi>
			        </mrow>
			        <mtext>y</mtext>
			      </msub>
			    </mrow>
			    <msub>
			      <mi>&#x03B3;<!-- γ --></mi>
			      <mrow class="MJX-TeXAtom-ORD">
			        <mtext>m0</mtext>
			      </mrow>
			    </msub>
			  </mfrac>
			  <mo>&gt;</mo>
			  <mtext>Force in flange</mtext>
			</math> 

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>b</mi>
						    <mtext>f</mtext>
						  </msub>
						</math> = Width of flange <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>n</mi>
						</math> = Number of bolts in flange <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>d</mi>
						    <mtext>0</mtext>
						  </msub>
						</math> = Diameter of the bolt hole <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>t</mi>
						    <mtext>f</mtext>
						  </msub>
						</math> = Thickness of flange <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m0</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor against yield stress and buckling <br>


	
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step13_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step13-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step13_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step13_feedback');
	$query->condition('uid', $user->uid);
	$form_step13_data = $query->execute();
	if ($form_step13_data)
	{
		if ($step13_data = $form_step13_data->fetchObject())
		{
			$form['step13_field1_fieldset']['step13_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step13_field1_fieldset']['step13_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step13_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step13_field1_fieldset']['step13_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step13_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step13_field1_fieldset\\[step13_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step13_data->id, $step13_data->data_relation);
			$icom = 1;
			$form['step13_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step13_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step13_num_comment']))
			{
				$form_state['step13_num_comment'] = 1;
			} //empty($form_state['step13_num_comment'])
			$step13_temp1 = 0;
			for ($step13_i = 0; $step13_i < $form_state['step13_num_comment']; $step13_i++)
			{
				$step13_temp1 = $step13_i;
				$form['step13_field1_fieldset'][$step13_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step13_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step13_field1_fieldset']["step13_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step13_temp1
			);
			$form['step13_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step13_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step13_comment_add_more_callback',
					'wrapper' => 'step13-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step13_num_comment'] > 1)
			{
				$form['step13_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step13_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step13_comment_add_more_callback',
						'wrapper' => 'step13-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step13_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step13_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step13_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step13_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step13_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step13_form_next_submit'
				)
			);
		} //$step13_data = $form_step13_data->fetchObject()
		else
		{
			$form['step13_field1_fieldset']['step13_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step13_field1_fieldset']['step13_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step13_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step13_field1_fieldset']['step13_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step13_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step13_field1_fieldset\\[step13_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step13_num_comment']))
			{
				$form_state['step13_num_comment'] = 1;
			} //empty($form_state['step13_num_comment'])
			$step13_temp1 = 0;
			for ($step13_i = 0; $step13_i < $form_state['step13_num_comment']; $step13_i++)
			{
				$step13_temp1 = $step13_i;
				$form['step13_field1_fieldset'][$step13_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step13_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step13_field1_fieldset']["step13_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step13_temp1
			);
			$form['step13_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step13_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step13_comment_add_more_callback',
					'wrapper' => 'step13-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step13_num_comment'] > 1)
			{
				$form['step13_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step13_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step13_comment_add_more_callback',
						'wrapper' => 'step13-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step13_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step13_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step13_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step13_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step13_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step13_form_next_submit'
				)
			);
		} //$step13_data = $form_step13_data->fetchObject()
	} //$form_step13_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step13_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step13_field1_fieldset']['step13_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step13_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step13_feedback');
	$query->condition('uid', $user->uid);
	$form_step13_data = $query->execute()->fetchObject();
	//var_dump($form_step12_data);die;
	if ($form_step13_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step13_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step13_field1_fieldset']['step13_field1_question1'],
			":question_ok_not_ok" => $v['step13_field1_fieldset']['step13_field1_question_ok'],
			":question_not_ok_comment" => $v['step13_field1_fieldset']['step13_field1_question_not_ok_comment'],
			":data_relation" => "step13"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step13_data->id
		));
		$form_step13_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++)
		{
			if ($v['step13_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step13_data->id,
					":number" => $i + $form_step13_comment_data->max + 1,
					":comment" => $v['step13_field1_fieldset'][$i]["comment"],
					":data_relation" => "step13",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step13_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++
	} //$form_step13_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step13_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step13_field1_fieldset']['step13_field1_question1'],
			":question_ok_not_ok" => $v['step13_field1_fieldset']['step13_field1_question_ok'],
			":question_not_ok_comment" => $v['step13_field1_fieldset']['step13_field1_question_not_ok_comment'],
			":data_relation" => "step13",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++)
		{
			if ($v['step13_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step13_field1_fieldset'][$i]["comment"],
					":data_relation" => "step13",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step13_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step12/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step13_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step13_field1_fieldset']['step13_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step13_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step13_feedback');
	$query->condition('uid', $user->uid);
	$form_step13_data = $query->execute()->fetchObject();
	//var_dump($form_step13_data);die;
	if ($form_step13_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step13_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step13_field1_fieldset']['step13_field1_question1'],
			":question_ok_not_ok" => $v['step13_field1_fieldset']['step13_field1_question_ok'],
			":question_not_ok_comment" => $v['step13_field1_fieldset']['step13_field1_question_not_ok_comment'],
			":data_relation" => "step13"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step13_data->id
		));
		$form_step13_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++)
		{
			if ($v['step13_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step13_data->id,
					":number" => $i + $form_step13_comment_data->max + 1,
					":comment" => $v['step13_field1_fieldset'][$i]["comment"],
					":data_relation" => "step13",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step13_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++
	} //$form_step7_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step13_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step13_field1_fieldset']['step13_field1_question1'],
			":question_ok_not_ok" => $v['step13_field1_fieldset']['step13_field1_question_ok'],
			":question_not_ok_comment" => $v['step13_field1_fieldset']['step13_field1_question_not_ok_comment'],
			":data_relation" => "step13",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++)
		{
			if ($v['step13_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step13_field1_fieldset'][$i]["comment"],
					":data_relation" => "step13",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step13_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step13_field1_fieldset']["step13_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step14/' . $user->uid;
}
/***************************************/
function step13_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step13_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step13_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step13_num_comment'] > 1)
	{
		$form_state['step13_num_comment']--;
	} //$form_state['step13_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step13_comment_add_more_callback($form, &$form_state)
{
	return $form['step13_field1_fieldset'];
}
/***************************************/
/***************************************** step 13 form ends ****************************/
/************************ Step 14 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step14_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('h. Flange splice plate checks > i. Strength against yielding of gross section > ii. Strength against rupture'));
	$img_path = '';
	$markup_text = '
	<b> <strong> h. Flange splice plate checks </strong>   </b> <br>
	&emsp; <b> <strong> i. Strength against yielding of gross section </strong> </b> [Reference: Clause 6.2 page 32, IS 800 : 2007] 
	<br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
			  <msub>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>T</mi>
			    </mrow>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mtext>dg</mtext>
			    </mrow>
			  </msub>
			  <mo>=</mo>
			  <mfrac>
			    <mrow>
			      <msub>
			        <mrow class="MJX-TeXAtom-ORD">
			          <mi>A</mi>
			        </mrow>
			        <mtext>g</mtext>
			      </msub>
			      <mspace width="thinmathspace" />
			      <msub>
			        <mrow class="MJX-TeXAtom-ORD">
			          <mi>f</mi>
			        </mrow>
			        <mtext>y</mtext>
			      </msub>
			    </mrow>
			    <msub>
			      <mi>&#x03B3;<!-- γ --></mi>
			      <mrow class="MJX-TeXAtom-ORD">
			        <mtext>m0</mtext>
			      </mrow>
			    </msub>
			  </mfrac>
			  <mo>&gt;</mo>
			  <mtext>Force in plate</mtext>
			</math>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mtext>g</mtext>
						  </msub>
						</math> = Gross area of cross section <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m0</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor for failure in tension by yielding <br><br>

	&emsp; <b> <strong> ii. Strength against rupture </strong> </b> [Reference: Clause 6.3.1 page 32, IS 800 : 2007] 
	<br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
			  <msub>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>T</mi>
			    </mrow>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mtext>dn</mtext>
			    </mrow>
			  </msub>
			  <mo>=</mo>
			  <mfrac>
			    <mrow>
			      <msub>
			        <mrow class="MJX-TeXAtom-ORD">
			          <mn>0.9</mn>
			          <mspace width="thinmathspace" />
			          <mi>A</mi>
			        </mrow>
			        <mtext>n</mtext>
			      </msub>
			      <mspace width="thinmathspace" />
			      <msub>
			        <mrow class="MJX-TeXAtom-ORD">
			          <mi>f</mi>
			        </mrow>
			        <mtext>u</mtext>
			      </msub>
			    </mrow>
			    <msub>
			      <mi>&#x03B3;<!-- γ --></mi>
			      <mrow class="MJX-TeXAtom-ORD">
			        <mtext>m1</mtext>
			      </mrow>
			    </msub>
			  </mfrac>
			  <mo>&gt;</mo>
			  <mtext>Force in plate</mtext>
			</math> 

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m1</mtext>
						    </mrow>
						  </msub>
						</math> =  Partial safety factor for failure at ultimate stress <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>u</mtext>
						  </msub>
						</math> = Ultimate stress of the material  <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>n</mi>
						</math> = Number of bolts in flange (in a row)<br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>d</mi>
						    <mtext>0</mtext>
						  </msub>
						</math> = Diameter of the bolt hole <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mtext>n</mtext>
						  </msub>
						</math> = Net effective area of the member = 
			<math xmlns="http://www.w3.org/1998/Math/MathML">

			  <mo stretchy="false">(</mo>
			  <msub>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>b</mi>
			    </mrow>
			    <mtext>f</mtext>
			  </msub>
			  <mo>&#x2212;<!-- − --></mo>
			  <mrow class="MJX-TeXAtom-ORD">
			    <mi>n</mi>
			  </mrow>
			  <mspace width="thinmathspace" />
			  <msub>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>d</mi>
			    </mrow>
			    <mn>0</mn>
			  </msub>
			  <mo stretchy="false">)</mo>
			  <mspace width="thinmathspace" />
			  <mrow class="MJX-TeXAtom-ORD">
			    <mi>t</mi>
			  </mrow>
			</math>  <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>b</mi>
						    <mtext>f</mtext>
						  </msub>
						</math> = Width of flange <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>t</mi>
						</math> = Thickness of flange splice plate<br>


	<hr>';
	// All the real form fields.
	$form = array();
	$form['step14_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step14-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step14_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step14_feedback');
	$query->condition('uid', $user->uid);
	$form_step14_data = $query->execute();
	if ($form_step14_data)
	{
		if ($step14_data = $form_step14_data->fetchObject())
		{
			$form['step14_field1_fieldset']['step14_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step14_field1_fieldset']['step14_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step14_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step14_field1_fieldset']['step14_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step14_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step14_field1_fieldset\\[step14_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step14_data->id, $step14_data->data_relation);
			$icom = 1;
			$form['step14_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step14_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step14_num_comment']))
			{
				$form_state['step14_num_comment'] = 1;
			} //empty($form_state['step14_num_comment'])
			$step14_temp1 = 0;
			for ($step14_i = 0; $step14_i < $form_state['step14_num_comment']; $step14_i++)
			{
				$step14_temp1 = $step14_i;
				$form['step14_field1_fieldset'][$step14_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step14_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step14_field1_fieldset']["step14_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step14_temp1
			);
			$form['step14_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step14_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step14_comment_add_more_callback',
					'wrapper' => 'step14-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step14_num_comment'] > 1)
			{
				$form['step14_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step14_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step14_comment_add_more_callback',
						'wrapper' => 'step14-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step14_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step14_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step14_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step14_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step14_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step14_form_next_submit'
				)
			);
		} //$step14_data = $form_step14_data->fetchObject()
		else
		{
			$form['step14_field1_fieldset']['step14_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step14_field1_fieldset']['step14_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step14_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step14_field1_fieldset']['step14_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step14_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step14_field1_fieldset\\[step14_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step14_num_comment']))
			{
				$form_state['step14_num_comment'] = 1;
			} //empty($form_state['step14_num_comment'])
			$step14_temp1 = 0;
			for ($step14_i = 0; $step14_i < $form_state['step14_num_comment']; $step14_i++)
			{
				$step14_temp1 = $step14_i;
				$form['step14_field1_fieldset'][$step14_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step14_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step14_field1_fieldset']["step14_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step14_temp1
			);
			$form['step14_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step14_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step14_comment_add_more_callback',
					'wrapper' => 'step14-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step14_num_comment'] > 1)
			{
				$form['step14_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step14_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step14_comment_add_more_callback',
						'wrapper' => 'step14-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step14_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step14_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step14_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step14_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step14_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step14_form_next_submit'
				)
			);
		} //$step14_data = $form_step14_data->fetchObject()
	} //$form_step14_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step14_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step14_field1_fieldset']['step14_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step14_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step14_feedback');
	$query->condition('uid', $user->uid);
	$form_step14_data = $query->execute()->fetchObject();
	//var_dump($form_step14_data);die;
	if ($form_step14_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step14_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step14_field1_fieldset']['step14_field1_question1'],
			":question_ok_not_ok" => $v['step14_field1_fieldset']['step14_field1_question_ok'],
			":question_not_ok_comment" => $v['step14_field1_fieldset']['step14_field1_question_not_ok_comment'],
			":data_relation" => "step14"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step14_data->id
		));
		$form_step14_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++)
		{
			if ($v['step14_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step14_data->id,
					":number" => $i + $form_step14_comment_data->max + 1,
					":comment" => $v['step14_field1_fieldset'][$i]["comment"],
					":data_relation" => "step14",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step14_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++
	} //$form_step14_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step14_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step14_field1_fieldset']['step14_field1_question1'],
			":question_ok_not_ok" => $v['step14_field1_fieldset']['step14_field1_question_ok'],
			":question_not_ok_comment" => $v['step14_field1_fieldset']['step14_field1_question_not_ok_comment'],
			":data_relation" => "step14",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++)
		{
			if ($v['step14_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step14_field1_fieldset'][$i]["comment"],
					":data_relation" => "step14",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step14_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step13/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step14_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step14_field1_fieldset']['step14_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step14_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step14_feedback');
	$query->condition('uid', $user->uid);
	$form_step14_data = $query->execute()->fetchObject();
	//var_dump($form_step14_data);die;
	if ($form_step14_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step14_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step14_field1_fieldset']['step14_field1_question1'],
			":question_ok_not_ok" => $v['step14_field1_fieldset']['step14_field1_question_ok'],
			":question_not_ok_comment" => $v['step14_field1_fieldset']['step14_field1_question_not_ok_comment'],
			":data_relation" => "step14"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step14_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++)
		{
			if ($v['step14_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step14_data->id,
					":number" => $i + $form_step14_comment_data->max + 1,
					":comment" => $v['step14_field1_fieldset'][$i]["comment"],
					":data_relation" => "step14",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step14_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++
	} //$form_step14_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step14_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step14_field1_fieldset']['step14_field1_question1'],
			":question_ok_not_ok" => $v['step14_field1_fieldset']['step14_field1_question_ok'],
			":question_not_ok_comment" => $v['step14_field1_fieldset']['step14_field1_question_not_ok_comment'],
			":data_relation" => "step14",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++)
		{
			if ($v['step14_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step14_field1_fieldset'][$i]["comment"],
					":data_relation" => "step14",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step14_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step14_field1_fieldset']["step14_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step15/' . $user->uid;
}
/***************************************/
function step14_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step14_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step14_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step14_num_comment'] > 1)
	{
		$form_state['step14_num_comment']--;
	} //$form_state['step14_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step14_comment_add_more_callback($form, &$form_state)
{
	return $form['step14_field1_fieldset'];
}
/***************************************/
/***************************************** step 14 form ends ****************************/
/************************ Step 15 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step15_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('h. Flange splice plate checks > iii. Block shear failure'));
	$img_path = '';
	$markup_text = '
	<b> <strong> h. Flange splice plate checks </strong> </b> <br>
	&emsp; <b> <strong> iii. Block shear failure </strong> [Reference: Clause 6.4.1 page 33, IS 800 : 2007] </b> <br>	
	&emsp;&emsp; Block shear capacity of the plate is should be greater than the force in flange <br>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db</mtext>
				    </mrow>
				  </msub>
				  <mo>&gt;</mo>
				  <mtext>Force in plate</mtext>
				  <mspace linebreak="newline" />
				</math> <br>

				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mtext>min</mtext>
				  <mspace width="thinmathspace" />
				  <mo stretchy="false">(</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db1</mtext>
				    </mrow>
				  </msub>
				  <mo>,</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db2</mtext>
				    </mrow>
				  </msub>
				  <mo stretchy="false">)</mo>
				</math> <br>

				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db1</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>vg</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>y</mtext>
				      </msub>
				    </mrow>
				    <mrow>
				      <msqrt>
				        <mn>3</mn>
				      </msqrt>
				      <mspace width="thinmathspace" />
				      <mspace width="thinmathspace" />
				      <msub>
				        <mi>&#x03B3;<!-- γ --></mi>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>m0</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				  <mo>+</mo>
				  <mfrac>
				    <mrow>
				      <mn>0.9</mn>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>tn</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>u</mtext>
				      </msub>
				    </mrow>
				    <msub>
				      <mi>&#x03B3;<!-- γ --></mi>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mtext>m1</mtext>
				      </mrow>
				    </msub>
				  </mfrac>
				</math> <br>

				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db2</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <mn>0.9</mn>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>vn</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>u</mtext>
				      </msub>
				    </mrow>
				    <mrow>
				      <msqrt>
				        <mn>3</mn>
				      </msqrt>
				      <mspace width="thinmathspace" />
				      <mspace width="thinmathspace" />
				      <msub>
				        <mi>&#x03B3;<!-- γ --></mi>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>m1</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				  <mo>+</mo>
				  <mfrac>
				    <mrow>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>tg</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>y</mtext>
				      </msub>
				    </mrow>
				    <msub>
				      <mi>&#x03B3;<!-- γ --></mi>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mtext>m0</mtext>
				      </mrow>
				    </msub>
				  </mfrac>
				</math>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>vg</mtext>
						    </mrow>
						  </msub>
						  <mo>,</mo>
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>vn</mtext>
						    </mrow>
						  </msub>
						</math> = minimum gross and net area in shear along bolt line parallel to external force respectively <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>tg</mtext>
						    </mrow>
						  </msub>
						  <mo>,</mo>
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>tn</mtext>
						    </mrow>
						  </msub>
						</math> = minimum gross and net area in tension from the bolt hole to the toe, end bolt line, perpendicular to the line of force <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>u</mtext>
						  </msub>
						</math> = Characteristic ultimate tensile stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m1</mtext>
						    </mrow>
						  </msub>
						</math> = partial safety factor for failure at ultimate stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m0</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor for failure in tension by yielding <br>

	<hr>';
	// All the real form fields.
	$form = array();
	$form['step15_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step15-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step15_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step15_feedback');
	$query->condition('uid', $user->uid);
	$form_step15_data = $query->execute();
	if ($form_step15_data)
	{
		if ($step15_data = $form_step15_data->fetchObject())
		{
			$form['step15_field1_fieldset']['step15_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step15_field1_fieldset']['step15_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step15_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step15_field1_fieldset']['step15_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step15_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step15_field1_fieldset\\[step15_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step15_data->id, $step15_data->data_relation);
			$icom = 1;
			$form['step15_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step15_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step15_num_comment']))
			{
				$form_state['step15_num_comment'] = 1;
			} //empty($form_state['step15_num_comment'])
			$step15_temp1 = 0;
			for ($step15_i = 0; $step15_i < $form_state['step15_num_comment']; $step15_i++)
			{
				$step15_temp1 = $step15_i;
				$form['step15_field1_fieldset'][$step15_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step15_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step15_field1_fieldset']["step15_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step15_temp1
			);
			$form['step15_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step15_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step15_comment_add_more_callback',
					'wrapper' => 'step15-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step15_num_comment'] > 1)
			{
				$form['step15_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step15_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step15_comment_add_more_callback',
						'wrapper' => 'step15-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step15_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step15_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step15_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step15_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step15_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step15_form_next_submit'
				)
			);
		} //$step15_data = $form_step15_data->fetchObject()
		else
		{
			$form['step15_field1_fieldset']['step15_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step15_field1_fieldset']['step15_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step15_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step15_field1_fieldset']['step15_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step15_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step15_field1_fieldset\\[step15_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step15_num_comment']))
			{
				$form_state['step15_num_comment'] = 1;
			} //empty($form_state['step15_num_comment'])
			$step15_temp1 = 0;
			for ($step15_i = 0; $step15_i < $form_state['step15_num_comment']; $step15_i++)
			{
				$step15_temp1 = $step15_i;
				$form['step15_field1_fieldset'][$step15_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step15_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step15_field1_fieldset']["step15_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step15_temp1
			);
			$form['step15_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step15_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step15_comment_add_more_callback',
					'wrapper' => 'step15-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step15_num_comment'] > 1)
			{
				$form['step15_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step15_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step15_comment_add_more_callback',
						'wrapper' => 'step15-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step15_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step15_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step15_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step15_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step15_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step15_form_next_submit'
				)
			);
		} //$step15_data = $form_step15_data->fetchObject()
	} //$form_step15_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step15_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step15_field1_fieldset']['step15_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step15_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step15_feedback');
	$query->condition('uid', $user->uid);
	$form_step15_data = $query->execute()->fetchObject();
	//var_dump($form_step15_data);die;
	if ($form_step15_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step15_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step15_field1_fieldset']['step15_field1_question1'],
			":question_ok_not_ok" => $v['step15_field1_fieldset']['step15_field1_question_ok'],
			":question_not_ok_comment" => $v['step15_field1_fieldset']['step15_field1_question_not_ok_comment'],
			":data_relation" => "step15"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step15_data->id
		));
		$form_step15_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++)
		{
			if ($v['step15_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step15_data->id,
					":number" => $i + $form_step15_comment_data->max + 1,
					":comment" => $v['step15_field1_fieldset'][$i]["comment"],
					":data_relation" => "step15",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step15_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++
	} //$form_step15_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step15_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step15_field1_fieldset']['step15_field1_question1'],
			":question_ok_not_ok" => $v['step15_field1_fieldset']['step15_field1_question_ok'],
			":question_not_ok_comment" => $v['step15_field1_fieldset']['step15_field1_question_not_ok_comment'],
			":data_relation" => "step15",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++)
		{
			if ($v['step15_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step15_field1_fieldset'][$i]["comment"],
					":data_relation" => "step15",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step15_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step14/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step15_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step15_field1_fieldset']['step15_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step15_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step15_feedback');
	$query->condition('uid', $user->uid);
	$form_step15_data = $query->execute()->fetchObject();
	//var_dump($form_step15_data);die;
	if ($form_step15_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step15_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step15_field1_fieldset']['step15_field1_question1'],
			":question_ok_not_ok" => $v['step15_field1_fieldset']['step15_field1_question_ok'],
			":question_not_ok_comment" => $v['step15_field1_fieldset']['step15_field1_question_not_ok_comment'],
			":data_relation" => "step15"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step15_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++)
		{
			if ($v['step15_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step15_data->id,
					":number" => $i + $form_step15_comment_data->max + 1,
					":comment" => $v['step15_field1_fieldset'][$i]["comment"],
					":data_relation" => "step15",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step15_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++
	} //$form_step15_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step15_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step15_field1_fieldset']['step15_field1_question1'],
			":question_ok_not_ok" => $v['step15_field1_fieldset']['step15_field1_question_ok'],
			":question_not_ok_comment" => $v['step15_field1_fieldset']['step15_field1_question_not_ok_comment'],
			":data_relation" => "step15",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++)
		{
			if ($v['step15_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step15_field1_fieldset'][$i]["comment"],
					":data_relation" => "step15",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step15_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step15_field1_fieldset']["step15_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step16/' . $user->uid;
}
/***************************************/
function step15_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step15_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step15_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step15_num_comment'] > 1)
	{
		$form_state['step15_num_comment']--;
	} //$form_state['step15_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step15_comment_add_more_callback($form, &$form_state)
{
	return $form['step15_field1_fieldset'];
}
/***************************************/
/***************************************** step 15 form ends ****************************/
/************************ Step 16 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step16_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of web splice > d. Bolt > vii. Shear capacity > viii. Bearing capacity > ix. Bolt value > x. Number of bolts'));
	$img_path = '';
	$markup_text = '
	<b> <strong> d. Bolt </strong> </b> <br>
	&emsp; <b> <strong> vii. Shear capacity  </strong></b> [Reference: Clause 10.4.3 page 76, IS 800 : 2007] 

</b> <br>

	<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <msub>
    <mrow class="MJX-TeXAtom-ORD">
      <mi>V</mi>
    </mrow>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>dsf</mtext>
    </mrow>
  </msub>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <msub>
        <mi>&#x03BC;<!-- μ --></mi>
        <mtext>f</mtext>
      </msub>
      <mspace width="thinmathspace" />
      <mspace width="thinmathspace" />
      <msub>
        <mrow class="MJX-TeXAtom-ORD">
          <mi>n</mi>
        </mrow>
        <mtext>e</mtext>
      </msub>
      <mspace width="thinmathspace" />
      <msub>
        <mrow class="MJX-TeXAtom-ORD">
          <mi>K</mi>
        </mrow>
        <mtext>h</mtext>
      </msub>
      <mspace width="thinmathspace" />
      <msub>
        <mrow class="MJX-TeXAtom-ORD">
          <mi>F</mi>
        </mrow>
        <mn>0</mn>
      </msub>
    </mrow>
    <msub>
      <mi>&#x03B3;<!-- γ --></mi>
      <mrow class="MJX-TeXAtom-ORD">
        <mtext>mf</mtext>
      </mrow>
    </msub>
  </mfrac>
</math>

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dsf</mtext>
						  </msub>
						</math> = Design shear capacity of a HSFG bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03BC;<!-- μ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>f</mtext>
						    </mrow>
						  </msub>
						</math> = Coefficient of friction (slip factor)  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>n</mi>
						    <mtext>e</mtext>
						  </msub>
						</math> = Number of effective interfaces offering frictional resistance to slip  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>mf</mtext>
						    </mrow>
						  </msub>
						</math> = 1.10 if slip resistance is designed at service load <br>
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; = 1.25 if slip resistance is designed at ultimate load	 <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>K</mi>
						    <mtext>h</mtext>
						  </msub>
						</math> = 1.0 for fasteners in clearance hole  <br>
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; = 0.85 for fasteners in oversized and short slotted holes <br>
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; = 0.7 for fasteners in long slotted holes loaded parallel to the slot <br> 
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>F</mi>
						    <mtext>0</mtext>
						  </msub>
						</math> = Minimum bolt tension (proof load) at installation and may be taken as 
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						 <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>nb</mtext>
						    </mrow>
						  </msub>
						  <mspace width="thinmathspace" />
						  <msub>
						    <mi>f</mi>
						    <mn>0</mn>
						  </msub>  <br>
						  </math>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mtext>nb</mtext>
						  </msub>
						</math> = Net area of the bolt at threads [Table 5.11 N. Subramanian]  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">						  
						    <mi>d</mi>				
						</math> = Diameter of the bolt  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>0</mtext>
						  </msub>
						</math> =  Proof stress   <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>ub</mtext>
						  </msub>
						</math> = Characteristic ultimate tensile stress of the bolt  <br>

	&emsp;&emsp;&emsp; <strong> This step is same as implemented in the shear connection modules (already reviewed). </strong>
	<br> 

	<br>
	&emsp;&emsp;&emsp; <strong> Note: </strong> <math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub>
    <mi>n</mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>e</mtext>
    </mrow>
  </msub>
</math> = 2, as there are two interface for web splice plates offering friction <br> <br>
	
	&emsp; <b> <strong> viii. Bearing capacity of Bolt </strong> </b> [Reference: Clause 10.3.4 page 75, IS  800 : 2007]  <br>


					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dpb</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <mn>2.5</mn>
				      <mspace width="thinmathspace" />
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>k</mi>
				        </mrow>
				        <mtext>b</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <mi>d</mi>
				      <mspace width="thinmathspace" />
				      <mi>t</mi>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>ub</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				    <msub>
				      <mi>&#x03B3;<!-- γ --></mi>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mtext>mb</mtext>
				      </mrow>
				    </msub>
				  </mfrac>
				</math>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dpb</mtext>
						  </msub>
						</math> = Design bearing strength of a bolt <br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
					  <msub>
					    <mi>k</mi>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>b</mtext>
					    </mrow>
					  </msub>
					</math>	is smaller of

					<math xmlns="http://www.w3.org/1998/Math/MathML">
					  <mo stretchy="false">(</mo>
					  <mi>e</mi>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo>/</mo>
					  </mrow>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mn>3</mn>
					    <msub>
					      <mi>d</mi>
					      <mn>0</mn>
					    </msub>
					  </mrow>
					  <mo stretchy="false">)</mo>
					  <mo>,</mo>
					  <mo stretchy="false">(</mo>
					  <mi>p</mi>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo>/</mo>
					  </mrow>
					  <mn>3</mn>
					  <msub>
					    <mi>d</mi>
					    <mn>0</mn>
					  </msub>
					  <mo stretchy="false">)</mo>
					  <mo>,</mo>
					  <mo stretchy="false">(</mo>
					  <msub>
					    <mi>f</mi>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>ub</mtext>
					    </mrow>
					  </msub>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo>/</mo>
					  </mrow>
					  <msub>
					    <mi>f</mi>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mtext>u</mtext>
					    </mrow>
					  </msub>
					  <mo stretchy="false">)</mo>
					  <mo>,</mo>
					  <mn>1.0</mn>
					</math> <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
					   <mi>e, p</mi>
					</math> = End and pitch distances of the fastener along bearing direction <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>d</mi>
						    <mtext>0</mtext>
						  </msub>
					</math> = Diameter of the bolt hole <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>ub</mtext>
						    </mrow>
						  </msub>
						  <mo>,</mo>
						  <msub>
						    <mi>f</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>u</mtext>
						    </mrow>
						  </msub>
					</math> = Ultimate tensile stress of the bolt and the ultimate tensile stress of the plate <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">						 
						    <mi>d</mi>						
					</math> = Nominal diameter of the bolt <br>
										&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>t</mi>
					</math> = Minimum (web thickness, thickness of web splice plate) <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>mb</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor for bolted connection with bearing type bolts <br>
&emsp;&emsp;&emsp; <strong> This step is same as implemented in the shear connection modules (already reviewed). </strong>
	<br><br>
	

&emsp; <b> <strong> ix. Bolt value </strong> </b>  <br>

&emsp;&emsp;&emsp;			The bolt value is taken as the minimum of bolt shear and bolt bearing capacity.
			  <math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mtext>min</mtext>
				  <mspace width="thinmathspace" />
				  <mo stretchy="false">(</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dsb</mtext>
				    </mrow>
				  </msub>
				  <mo>,</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dpb</mtext>
				    </mrow>
				  </msub>
				  <mo>,</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>dsf</mtext>
				    </mrow>
				  </msub>
				  <mo stretchy="false">)</mo>
				</math>
		&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>db</mtext>
						  </msub>
						</math> = Design strength of bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dsb</mtext>
						  </msub>
						</math> = Design shear capacity of bearing bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dpb</mtext>
						  </msub>
						</math> = Design bearing capacity of bolt <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>dsf</mtext>
						  </msub>
						</math> = Design shear capacity of friction grip bolt <br>	<br>

&emsp; <b> <strong> x. Number of bolts </strong> </b> <br> 

					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
					  <mi>n</mi>
					  <mo>=</mo>
					  <mtext>Ceiling</mtext>
					  <mspace width="thinmathspace" />
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo maxsize="2.047em" minsize="2.047em">[</mo>
					  </mrow>
					  <mfrac>
					    <mtext>Factored shear force</mtext>
					    <mtext>Bolt value</mtext>
					  </mfrac>
					  <mrow class="MJX-TeXAtom-ORD">
					    <mo maxsize="2.047em" minsize="2.047em">]</mo>
					  </mrow>
					</math>

&emsp;&emsp;&emsp; <strong> All the above steps are same as in flange splice plate design </strong> <br>

	
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step16_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step16-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step16_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step16_feedback');
	$query->condition('uid', $user->uid);
	$form_step16_data = $query->execute();
	if ($form_step16_data)
	{
		if ($step16_data = $form_step16_data->fetchObject())
		{
			$form['step16_field1_fieldset']['step16_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step16_field1_fieldset']['step16_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step16_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step16_field1_fieldset']['step16_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step16_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step16_field1_fieldset\\[step16_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step16_data->id, $step16_data->data_relation);
			$icom = 1;
			$form['step16_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step16_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step16_num_comment']))
			{
				$form_state['step16_num_comment'] = 1;
			} //empty($form_state['step16_num_comment'])
			$step16_temp1 = 0;
			for ($step16_i = 0; $step16_i < $form_state['step16_num_comment']; $step16_i++)
			{
				$step16_temp1 = $step16_i;
				$form['step16_field1_fieldset'][$step16_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step16_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step16_field1_fieldset']["step16_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step16_temp1
			);
			$form['step16_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step16_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step16_comment_add_more_callback',
					'wrapper' => 'step16-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step16_num_comment'] > 1)
			{
				$form['step16_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step16_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step16_comment_add_more_callback',
						'wrapper' => 'step16-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step16_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step16_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step16_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step16_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step16_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step16_form_next_submit'
				)
			);
		} //$step16_data = $form_step16_data->fetchObject()
		else
		{
			$form['step16_field1_fieldset']['step16_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step16_field1_fieldset']['step16_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step16_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step16_field1_fieldset']['step16_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step16_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step16_field1_fieldset\\[step16_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step16_num_comment']))
			{
				$form_state['step16_num_comment'] = 1;
			} //empty($form_state['step16_num_comment'])
			$step16_temp1 = 0;
			for ($step16_i = 0; $step16_i < $form_state['step16_num_comment']; $step16_i++)
			{
				$step16_temp1 = $step16_i;
				$form['step16_field1_fieldset'][$step16_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step16_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step16_field1_fieldset']["step16_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step16_temp1
			);
			$form['step16_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step16_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step16_comment_add_more_callback',
					'wrapper' => 'step16-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step16_num_comment'] > 1)
			{
				$form['step16_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step16_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step16_comment_add_more_callback',
						'wrapper' => 'step16-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step16_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step16_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step16_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step16_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step16_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step16_form_next_submit'
				)
			);
		} //$step16_data = $form_step16_data->fetchObject()
	} //$form_step16_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step16_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step16_field1_fieldset']['step16_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step16_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step16_feedback');
	$query->condition('uid', $user->uid);
	$form_step16_data = $query->execute()->fetchObject();
	//var_dump($form_step16_data);die;
	if ($form_step16_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step16_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step16_field1_fieldset']['step16_field1_question1'],
			":question_ok_not_ok" => $v['step16_field1_fieldset']['step16_field1_question_ok'],
			":question_not_ok_comment" => $v['step16_field1_fieldset']['step16_field1_question_not_ok_comment'],
			":data_relation" => "step16"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step16_data->id
		));
		$form_step16_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++)
		{
			if ($v['step16_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step16_data->id,
					":number" => $i + $form_step16_comment_data->max + 1,
					":comment" => $v['step16_field1_fieldset'][$i]["comment"],
					":data_relation" => "step16",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step16_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++
	} //$form_step16_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step16_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step16_field1_fieldset']['step16_field1_question1'],
			":question_ok_not_ok" => $v['step16_field1_fieldset']['step16_field1_question_ok'],
			":question_not_ok_comment" => $v['step16_field1_fieldset']['step16_field1_question_not_ok_comment'],
			":data_relation" => "step16",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++)
		{
			if ($v['step16_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step16_field1_fieldset'][$i]["comment"],
					":data_relation" => "step16",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step16_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step15/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step16_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step16_field1_fieldset']['step16_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step16_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step16_feedback');
	$query->condition('uid', $user->uid);
	$form_step16_data = $query->execute()->fetchObject();
	//var_dump($form_step16_data);die;
	if ($form_step16_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step16_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step16_field1_fieldset']['step16_field1_question1'],
			":question_ok_not_ok" => $v['step16_field1_fieldset']['step16_field1_question_ok'],
			":question_not_ok_comment" => $v['step16_field1_fieldset']['step16_field1_question_not_ok_comment'],
			":data_relation" => "step16"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step16_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++)
		{
			if ($v['step16_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step16_data->id,
					":number" => $i + $form_step16_comment_data->max + 1,
					":comment" => $v['step16_field1_fieldset'][$i]["comment"],
					":data_relation" => "step16",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step16_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++
	} //$form_step16_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step16_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step16_field1_fieldset']['step16_field1_question1'],
			":question_ok_not_ok" => $v['step16_field1_fieldset']['step16_field1_question_ok'],
			":question_not_ok_comment" => $v['step16_field1_fieldset']['step16_field1_question_not_ok_comment'],
			":data_relation" => "step16",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++)
		{
			if ($v['step16_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step16_field1_fieldset'][$i]["comment"],
					":data_relation" => "step16",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step16_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step16_field1_fieldset']["step16_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step17/' . $user->uid;
}
/***************************************/
function step16_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step16_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step16_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step16_num_comment'] > 1)
	{
		$form_state['step16_num_comment']--;
	} //$form_state['step16_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step16_comment_add_more_callback($form, &$form_state)
{
	return $form['step16_field1_fieldset'];
}
/***************************************/
/***************************************** step 16 form ends ****************************/
/************************ Step 17 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step17_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of web splice > i. Thickness of web splice plate > i. Minimum thickness > ii. Maximum thickness'));
	$img_path = '';
	$markup_text = '
	<b> <strong> i. Thickness of web splice plate </strong> </b> <br>
	&emsp; <b> <strong> i. a. Minimum thickness </strong> </b> [Reference: N. Subramanian, section 5.7.7 page 373]  <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>t</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>p, min</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <mn>5</mn>
				      <mspace width="thinmathspace" />
				      <mi>F</mi>
				    </mrow>
				    <mrow>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>y</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>h</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>p, min</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				</math> 
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>t</mi>
						    <mtext>p, min</mtext>
						  </msub>
						</math> = Minimum thickness of web splice plate <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						<mi>F</mi>
						</math> = Factored shear force  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>h</mi>
						    <mtext>p, min</mtext>
						  </msub>
						</math> = Minimum web splice plate height <br>	<br>
 
					&emsp; <b> <strong> i. b. Minimum thickness </strong> </b> [Reference: Previous DDCL, fin plate connection]  <br>	<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
							  <msub>
							    <mrow class="MJX-TeXAtom-ORD">
							      <mi>t</mi>
							    </mrow>
							    <mrow class="MJX-TeXAtom-ORD">
							      <mtext>p, min</mtext>
							    </mrow>
							  </msub>
							  <mo>&gt;</mo>
							  <msub>
							    <mrow class="MJX-TeXAtom-ORD">
							      <mi>t</mi>
							    </mrow>
							    <mrow class="MJX-TeXAtom-ORD">
							      <mtext>w</mtext>
							    </mrow>
							  </msub>
							</math>
							&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
							Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>t</mi>
						    <mtext>w</mtext>
						  </msub>
						</math> = Thickness of beam web <br> 
						&emsp;&emsp; <strong> Note: </strong> <br>
	&emsp;&emsp;&emsp; 1. It is assumed that greater plate thickness ensure that the plate is stronger than the beam web against shear. <br>
	&emsp;&emsp;&emsp; 2. It is assumed that the beam is designed to be safe against shear. <br> <br>

	&emsp; <b> <strong> ii. Maximum thickness </strong> </b> [Reference:  Handbook on structural steel detailing, INSDAG - Chapter 5, section  5.2.3 page 5.7]  <br>
							<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mi>t</mi>
						    </mrow>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>p, max</mtext>
						    </mrow>
						  </msub>
						  <mo>=</mo>
						  <mn>0.5</mn>
						  <mspace width="thinmathspace" />
						  <mi>d</mi>
						</math> 
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
							Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>t</mi>
						    <mtext>p, max</mtext>
						  </msub>
						</math> = Maximum thickness of web splice plate <br> 
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>d</mi>
						</math> = Nominal bolt diameter <br> 

							

	<hr>';
	// All the real form fields.
	$form = array();
	$form['step17_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step17-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step17_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step17_feedback');
	$query->condition('uid', $user->uid);
	$form_step17_data = $query->execute();
	if ($form_step17_data)
	{
		if ($step17_data = $form_step17_data->fetchObject())
		{
			$form['step17_field1_fieldset']['step17_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step17_field1_fieldset']['step17_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step17_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step17_field1_fieldset']['step17_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step17_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step17_field1_fieldset\\[step17_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step17_data->id, $step17_data->data_relation);
			$icom = 1;
			$form['step17_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step17_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step17_num_comment']))
			{
				$form_state['step17_num_comment'] = 1;
			} //empty($form_state['step17_num_comment'])
			$step17_temp1 = 0;
			for ($step17_i = 0; $step17_i < $form_state['step17_num_comment']; $step17_i++)
			{
				$step17_temp1 = $step17_i;
				$form['step17_field1_fieldset'][$step17_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step17_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step17_field1_fieldset']["step17_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step17_temp1
			);
			$form['step17_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step17_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step17_comment_add_more_callback',
					'wrapper' => 'step17-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step17_num_comment'] > 1)
			{
				$form['step17_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step17_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step17_comment_add_more_callback',
						'wrapper' => 'step17-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step17_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step17_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step17_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step17_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step17_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step17_form_next_submit'
				)
			);
		} //$step17_data = $form_step17_data->fetchObject()
		else
		{
			$form['step17_field1_fieldset']['step17_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step17_field1_fieldset']['step17_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step17_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step17_field1_fieldset']['step17_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step17_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step17_field1_fieldset\\[step17_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step17_num_comment']))
			{
				$form_state['step17_num_comment'] = 1;
			} //empty($form_state['step17_num_comment'])
			$step17_temp1 = 0;
			for ($step17_i = 0; $step17_i < $form_state['step17_num_comment']; $step17_i++)
			{
				$step17_temp1 = $step17_i;
				$form['step17_field1_fieldset'][$step17_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step17_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step17_field1_fieldset']["step17_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step17_temp1
			);
			$form['step17_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step17_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step17_comment_add_more_callback',
					'wrapper' => 'step17-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step17_num_comment'] > 1)
			{
				$form['step17_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step17_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step17_comment_add_more_callback',
						'wrapper' => 'step17-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step17_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step17_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step17_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step17_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step17_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step17_form_next_submit'
				)
			);
		} //$step17_data = $form_step17_data->fetchObject()
	} //$form_step17_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step17_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step17_field1_fieldset']['step17_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step17_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step17_feedback');
	$query->condition('uid', $user->uid);
	$form_step17_data = $query->execute()->fetchObject();
	//var_dump($form_step17_data);die;
	if ($form_step17_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step17_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step17_field1_fieldset']['step17_field1_question1'],
			":question_ok_not_ok" => $v['step17_field1_fieldset']['step17_field1_question_ok'],
			":question_not_ok_comment" => $v['step17_field1_fieldset']['step17_field1_question_not_ok_comment'],
			":data_relation" => "step17"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step17_data->id
		));
		$form_step17_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++)
		{
			if ($v['step17_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step17_data->id,
					":number" => $i + $form_step17_comment_data->max + 1,
					":comment" => $v['step17_field1_fieldset'][$i]["comment"],
					":data_relation" => "step17",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step17_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++
	} //$form_step17_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step17_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step17_field1_fieldset']['step17_field1_question1'],
			":question_ok_not_ok" => $v['step17_field1_fieldset']['step17_field1_question_ok'],
			":question_not_ok_comment" => $v['step17_field1_fieldset']['step17_field1_question_not_ok_comment'],
			":data_relation" => "step17",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++)
		{
			if ($v['step17_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step17_field1_fieldset'][$i]["comment"],
					":data_relation" => "step17",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step17_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step16/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step17_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step17_field1_fieldset']['step17_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step17_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step17_feedback');
	$query->condition('uid', $user->uid);
	$form_step17_data = $query->execute()->fetchObject();
	//var_dump($form_step17_data);die;
	if ($form_step17_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step17_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step17_field1_fieldset']['step17_field1_question1'],
			":question_ok_not_ok" => $v['step17_field1_fieldset']['step17_field1_question_ok'],
			":question_not_ok_comment" => $v['step17_field1_fieldset']['step17_field1_question_not_ok_comment'],
			":data_relation" => "step17"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step17_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++)
		{
			if ($v['step17_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step17_data->id,
					":number" => $i + $form_step17_comment_data->max + 1,
					":comment" => $v['step17_field1_fieldset'][$i]["comment"],
					":data_relation" => "step17",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step17_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++
	} //$form_step17_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step17_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step17_field1_fieldset']['step17_field1_question1'],
			":question_ok_not_ok" => $v['step17_field1_fieldset']['step17_field1_question_ok'],
			":question_not_ok_comment" => $v['step17_field1_fieldset']['step17_field1_question_not_ok_comment'],
			":data_relation" => "step17",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++)
		{
			if ($v['step17_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step17_field1_fieldset'][$i]["comment"],
					":data_relation" => "step17",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step17_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step17_field1_fieldset']["step17_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step18/' . $user->uid;
}
/***************************************/
function step17_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step17_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step17_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step17_num_comment'] > 1)
	{
		$form_state['step17_num_comment']--;
	} //$form_state['step17_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step17_comment_add_more_callback($form, &$form_state)
{
	return $form['step17_field1_fieldset'];
}
/***************************************/
/***************************************** step 17 form ends ****************************/
/************************ Step 18 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step18_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of web splice plate > d. Bolt > xi. Re-Check for bolt value (long joints)'));
	$markup_text = '
	
	<b> <strong> d. Bolt </strong> </b> <br>
	&emsp; <b> <strong> xi. Re-Check for bolt value (long joints) </strong> [Reference: Clause 10.3.3.1 page 75, IS 800 : 2007] </b> <br>
	&emsp;&emsp; Shear capacity (bearing and HSFG bolt) and bearing capacity of the bolts are evaluated again considering long joint provision. <br>
	&emsp;&emsp;When the length of joint, <math xmlns="http://www.w3.org/1998/Math/MathML" >
  <msub>
    <mi>l</mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>j</mtext>
    </mrow>
  </msub>
</math>  of a splice or end connection in compression or tension element containing more than two bolts (that is distance between the first and last rows of bolts in the joint, measured in the direction of load transfer) exceeds 15d in the direction of load, the nominal shear capacity <math xmlns="http://www.w3.org/1998/Math/MathML" >
  <msub>
    <mi>V</mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>db</mtext>
    </mrow>
  </msub>
</math> shall be reduced by the factor <math xmlns="http://www.w3.org/1998/Math/MathML">
  <msub>
    <mi>&#x03B2;<!-- β --></mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>lj</mtext>
    </mrow>
  </msub>
</math>. <br>

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <msub>
    <mi>&#x03B2;<!-- β --></mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>lj</mtext>
    </mrow>
  </msub>
  <mo>=</mo>
  <mn>1.075</mn>
  <mo>&#x2212;<!-- − --></mo>
  <mfrac>
    <msub>
      <mrow class="MJX-TeXAtom-ORD">
        <mi>l</mi>
      </mrow>
      <mtext>j</mtext>
    </msub>
    <mrow class="MJX-TeXAtom-ORD">
      <mn>200</mn>
      <mspace width="thinmathspace" />
      <mi>d</mi>
    </mrow>
  </mfrac>
  <mspace width="thinmathspace" />
  <mspace width="thinmathspace" />
  <mspace width="thinmathspace" />
  <mtext>But</mtext>
  <mo>,</mo>
  <mn>0.75</mn>
  <mo>&#x2264;<!-- ≤ --></mo>
  <msub>
    <mi>&#x03B2;<!-- β --></mi>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>lj</mtext>
    </mrow>
  </msub>
  <mo>&#x2264;<!-- ≤ --></mo>
  <mn>1.0</mn>
</math>
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step18_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step18-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step18_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step18_feedback');
	$query->condition('uid', $user->uid);
	$form_step18_data = $query->execute();
	if ($form_step18_data)
	{
		if ($step18_data = $form_step18_data->fetchObject())
		{
			$form['step18_field1_fieldset']['step18_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step18_field1_fieldset']['step18_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step18_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step18_field1_fieldset']['step18_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step18_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step18_field1_fieldset\\[step18_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step18_data->id, $step18_data->data_relation);
			$icom = 1;
			$form['step18_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step18_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step18_num_comment']))
			{
				$form_state['step18_num_comment'] = 1;
			} //empty($form_state['step18_num_comment'])
			$step18_temp1 = 0;
			for ($step18_i = 0; $step18_i < $form_state['step18_num_comment']; $step18_i++)
			{
				$step18_temp1 = $step18_i;
				$form['step18_field1_fieldset'][$step18_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step18_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step18_field1_fieldset']["step18_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step18_temp1
			);
			$form['step18_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step18_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step18_comment_add_more_callback',
					'wrapper' => 'step18-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step18_num_comment'] > 1)
			{
				$form['step18_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step18_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step18_comment_add_more_callback',
						'wrapper' => 'step18-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step18_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step18_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step18_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step18_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step18_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step18_form_next_submit'
				)
			);
		} //$step18_data = $form_step18_data->fetchObject()
		else
		{
			$form['step18_field1_fieldset']['step18_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step18_field1_fieldset']['step18_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step18_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step18_field1_fieldset']['step18_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step18_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step18_field1_fieldset\\[step18_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step18_num_comment']))
			{
				$form_state['step18_num_comment'] = 1;
			} //empty($form_state['step18_num_comment'])
			$step18_temp1 = 0;
			for ($step18_i = 0; $step18_i < $form_state['step18_num_comment']; $step18_i++)
			{
				$step18_temp1 = $step18_i;
				$form['step18_field1_fieldset'][$step18_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step18_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step18_field1_fieldset']["step18_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step18_temp1
			);
			$form['step18_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step18_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step18_comment_add_more_callback',
					'wrapper' => 'step18-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step18_num_comment'] > 1)
			{
				$form['step18_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step18_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step18_comment_add_more_callback',
						'wrapper' => 'step18-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step18_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step18_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step18_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step18_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step18_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step18_form_next_submit'
				)
			);
		} //$step18_data = $form_step18_data->fetchObject()
	} //$form_step18_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step18_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step18_field1_fieldset']['step18_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step18_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step18_feedback');
	$query->condition('uid', $user->uid);
	$form_step18_data = $query->execute()->fetchObject();
	//var_dump($form_step18_data);die;
	if ($form_step18_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step18_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step18_field1_fieldset']['step18_field1_question1'],
			":question_ok_not_ok" => $v['step18_field1_fieldset']['step18_field1_question_ok'],
			":question_not_ok_comment" => $v['step18_field1_fieldset']['step18_field1_question_not_ok_comment'],
			":data_relation" => "step18"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step18_data->id
		));
		$form_step18_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++)
		{
			if ($v['step18_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step18_data->id,
					":number" => $i + $form_step18_comment_data->max + 1,
					":comment" => $v['step18_field1_fieldset'][$i]["comment"],
					":data_relation" => "step18",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step18_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++
	} //$form_step18_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step18_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step18_field1_fieldset']['step18_field1_question1'],
			":question_ok_not_ok" => $v['step18_field1_fieldset']['step18_field1_question_ok'],
			":question_not_ok_comment" => $v['step18_field1_fieldset']['step18_field1_question_not_ok_comment'],
			":data_relation" => "step18",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++)
		{
			if ($v['step18_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step18_field1_fieldset'][$i]["comment"],
					":data_relation" => "step18",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step18_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step17/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step18_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step18_field1_fieldset']['step18_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step18_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step18_feedback');
	$query->condition('uid', $user->uid);
	$form_step18_data = $query->execute()->fetchObject();
	//var_dump($form_step18_data);die;
	if ($form_step18_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step18_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step18_field1_fieldset']['step18_field1_question1'],
			":question_ok_not_ok" => $v['step18_field1_fieldset']['step18_field1_question_ok'],
			":question_not_ok_comment" => $v['step18_field1_fieldset']['step18_field1_question_not_ok_comment'],
			":data_relation" => "step18"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step18_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++)
		{
			if ($v['step18_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step18_data->id,
					":number" => $i + $form_step18_comment_data->max + 1,
					":comment" => $v['step18_field1_fieldset'][$i]["comment"],
					":data_relation" => "step18",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step18_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++
	} //$form_step18_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step18_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step18_field1_fieldset']['step18_field1_question1'],
			":question_ok_not_ok" => $v['step18_field1_fieldset']['step18_field1_question_ok'],
			":question_not_ok_comment" => $v['step18_field1_fieldset']['step18_field1_question_not_ok_comment'],
			":data_relation" => "step18",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++)
		{
			if ($v['step18_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step18_field1_fieldset'][$i]["comment"],
					":data_relation" => "step18",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step18_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step18_field1_fieldset']["step18_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step19/' . $user->uid;
}
/***************************************/
function step18_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step18_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step18_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step18_num_comment'] > 1)
	{
		$form_state['step18_num_comment']--;
	} //$form_state['step18_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step18_comment_add_more_callback($form, &$form_state)
{
	return $form['step18_field1_fieldset'];
}
/***************************************/
/***************************************** step 18 form ends ****************************/
/************************ Step 19 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step19_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Design of web splice > d. Bolt > xii. Factored resultant shear force'));
	$img_path = '';
	$markup_text = '
	<b> <strong> d. Bolt </strong></b> <br>
	&emsp; <b> <strong> xii. Factored resultant shear force </strong></b> [Ref: M.L. Gambhir (page 10.85) and N. Subramanian (page 428)]  <br>
	&emsp;&emsp; 		The bolts have to resist a resultant shear force arising due to the factored shear force (vertical, 						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>V</mtext>
						  </msub>
						</math> ) and shear force arising due to the bolt eccentricity (horizontal, 				<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>H</mtext>
						  </msub>
						</math>). <br>

	&emsp;&emsp;&emsp;&emsp; <strong> a. Horizontal shear force 				(<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>H</mtext>
						  </msub>
						</math>) </strong> <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mtext>H</mtext>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>V</mi>
				        </mrow>
				        <mtext>x</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>e</mi>
				        </mrow>
				        <mtext>x</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>r</mi>
				        </mrow>
				        <mtext>i</mtext>
				      </msub>
				    </mrow>
				    <mrow>
				      <mo>&#x2211;<!-- ∑ --></mo>
				      <msubsup>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>r</mi>
				        </mrow>
				        <mtext>i</mtext>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mspace width="thinmathspace" />
				          <mn>2</mn>
				        </mrow>
				      </msubsup>
				    </mrow>
				  </mfrac>
				</math>

				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>x</mtext>
						  </msub>
						</math> = Applied shear force <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						<msub>
						    <mi>e</mi>
						    <mtext>x</mtext>
						  </msub>
						</math> = Eccentricity of bolt group  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>r</mi>
						    <mtext>i</mtext>
						  </msub>
						</math> = Distance of each bolt from CG of the bolt group <br>	

	&emsp;&emsp;&emsp;&emsp; <strong> b. vertical shear force 				(<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>V</mtext>
						  </msub>
						</math>) </strong> <br>
			<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
			  <msub>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>V</mi>
			    </mrow>
			    <mtext>V</mtext>
			  </msub>
			  <mo>=</mo>
			  <mfrac>
			    <msub>
			      <mrow class="MJX-TeXAtom-ORD">
			        <mi>V</mi>
			      </mrow>
			      <mtext>x</mtext>
			    </msub>
			    <mrow class="MJX-TeXAtom-ORD">
			      <mi>n</mi>
			    </mrow>
			  </mfrac>
			</math>
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>n</mi>
						</math> = Number of bolts <br>
<br>
&emsp;&emsp; <strong> Factored resultant shear force (<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>R</mtext>
						  </msub>
						</math>) </strong> <br>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
					  <msub>
					    <mrow class="MJX-TeXAtom-ORD">
					      <mi>V</mi>
					    </mrow>
					    <mtext>R</mtext>
					  </msub>
					  <mo>=</mo>
					  <msqrt>
					    <msup>
					      <mrow class="MJX-TeXAtom-ORD">
					        <msub>
					          <mrow class="MJX-TeXAtom-ORD">
					            <mi>V</mi>
					          </mrow>
					          <mtext>H</mtext>
					        </msub>
					      </mrow>
					      <mn>2</mn>
					    </msup>
					    <mo>+</mo>
					    <msup>
					      <mrow class="MJX-TeXAtom-ORD">
					        <msub>
					          <mrow class="MJX-TeXAtom-ORD">
					            <mi>V</mi>
					          </mrow>
					          <mtext>V</mtext>
					        </msub>
					      </mrow>
					      <mn>2</mn>
					    </msup>
					  </msqrt>
					  <mo>&lt;</mo>
					  <mtext>Bolt value</mtext>
					</math>



	<hr>';
	// All the real form fields.
	$form = array();
	$form['step19_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step19-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step19_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step19_feedback');
	$query->condition('uid', $user->uid);
	$form_step19_data = $query->execute();
	if ($form_step19_data)
	{
		if ($step19_data = $form_step19_data->fetchObject())
		{
			$form['step19_field1_fieldset']['step19_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step19_field1_fieldset']['step19_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step19_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step19_field1_fieldset']['step19_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step19_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step19_field1_fieldset\\[step19_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step19_data->id, $step19_data->data_relation);
			$icom = 1;
			$form['step19_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step19_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step19_num_comment']))
			{
				$form_state['step19_num_comment'] = 1;
			} //empty($form_state['step19_num_comment'])
			$step19_temp1 = 0;
			for ($step19_i = 0; $step19_i < $form_state['step19_num_comment']; $step19_i++)
			{
				$step19_temp1 = $step19_i;
				$form['step19_field1_fieldset'][$step19_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step19_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step19_field1_fieldset']["step19_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step19_temp1
			);
			$form['step19_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step19_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step19_comment_add_more_callback',
					'wrapper' => 'step19-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step19_num_comment'] > 1)
			{
				$form['step19_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step19_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step19_comment_add_more_callback',
						'wrapper' => 'step19-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step19_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step19_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step19_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step19_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step19_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step19_form_next_submit'
				)
			);
		} //$step19_data = $form_step19_data->fetchObject()
		else
		{
			$form['step19_field1_fieldset']['step19_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step19_field1_fieldset']['step19_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step19_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step19_field1_fieldset']['step19_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step19_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step19_field1_fieldset\\[step19_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step19_num_comment']))
			{
				$form_state['step19_num_comment'] = 1;
			} //empty($form_state['step19_num_comment'])
			$step19_temp1 = 0;
			for ($step19_i = 0; $step19_i < $form_state['step19_num_comment']; $step19_i++)
			{
				$step19_temp1 = $step19_i;
				$form['step19_field1_fieldset'][$step19_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step19_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step19_field1_fieldset']["step19_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step19_temp1
			);
			$form['step19_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step19_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step19_comment_add_more_callback',
					'wrapper' => 'step19-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step19_num_comment'] > 1)
			{
				$form['step19_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step19_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step19_comment_add_more_callback',
						'wrapper' => 'step19-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step19_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step19_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step19_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step19_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step19_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step19_form_next_submit'
				)
			);
		} //$step19_data = $form_step19_data->fetchObject()
	} //$form_step19_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step19_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step19_field1_fieldset']['step19_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step19_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step19_feedback');
	$query->condition('uid', $user->uid);
	$form_step19_data = $query->execute()->fetchObject();
	//var_dump($form_step19_data);die;
	if ($form_step19_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step19_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step19_field1_fieldset']['step19_field1_question1'],
			":question_ok_not_ok" => $v['step19_field1_fieldset']['step19_field1_question_ok'],
			":question_not_ok_comment" => $v['step19_field1_fieldset']['step19_field1_question_not_ok_comment'],
			":data_relation" => "step19"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step19_data->id
		));
		$form_step19_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++)
		{
			if ($v['step19_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step19_data->id,
					":number" => $i + $form_step19_comment_data->max + 1,
					":comment" => $v['step19_field1_fieldset'][$i]["comment"],
					":data_relation" => "step19",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step19_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++
	} //$form_step19_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step19_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step19_field1_fieldset']['step19_field1_question1'],
			":question_ok_not_ok" => $v['step19_field1_fieldset']['step19_field1_question_ok'],
			":question_not_ok_comment" => $v['step19_field1_fieldset']['step19_field1_question_not_ok_comment'],
			":data_relation" => "step19",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++)
		{
			if ($v['step19_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step19_field1_fieldset'][$i]["comment"],
					":data_relation" => "step19",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step19_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step18/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step19_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step19_field1_fieldset']['step19_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step19_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step19_feedback');
	$query->condition('uid', $user->uid);
	$form_step19_data = $query->execute()->fetchObject();
	//var_dump($form_step19_data);die;
	if ($form_step19_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step19_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step19_field1_fieldset']['step19_field1_question1'],
			":question_ok_not_ok" => $v['step19_field1_fieldset']['step19_field1_question_ok'],
			":question_not_ok_comment" => $v['step19_field1_fieldset']['step19_field1_question_not_ok_comment'],
			":data_relation" => "step19"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step19_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++)
		{
			if ($v['step19_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step19_data->id,
					":number" => $i + $form_step19_comment_data->max + 1,
					":comment" => $v['step19_field1_fieldset'][$i]["comment"],
					":data_relation" => "step19",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step19_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++
	} //$form_step19_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step19_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step19_field1_fieldset']['step19_field1_question1'],
			":question_ok_not_ok" => $v['step19_field1_fieldset']['step19_field1_question_ok'],
			":question_not_ok_comment" => $v['step19_field1_fieldset']['step19_field1_question_not_ok_comment'],
			":data_relation" => "step19",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++)
		{
			if ($v['step19_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step19_field1_fieldset'][$i]["comment"],
					":data_relation" => "step19",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step19_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step19_field1_fieldset']["step19_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step20/' . $user->uid;
}
/***************************************/
function step19_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step19_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step19_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step19_num_comment'] > 1)
	{
		$form_state['step19_num_comment']--;
	} //$form_state['step19_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step19_comment_add_more_callback($form, &$form_state)
{
	return $form['step19_field1_fieldset'];
}
/***************************************/
/***************************************** step 19 form ends ****************************/
/************************ Step 20 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step20_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('j. Web splice plate check > i. Shear yielding > ii. Shear rupture'));
	$img_path = '';
	$markup_text = '
	<b> <strong> j. Web splice plate checks </strong></b> <br>
	&emsp; <b> <strong> i. Shear yielding </strong></b>  [Reference: Clause 8.4.1, IS 800:2007, fin plate connection documentation] <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>V</mi>
				    </mrow>
				    <mtext>p</mtext>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <mn>0.6</mn>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mtext>v</mtext>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>y</mtext>
				      </msub>
				    </mrow>
				    <mrow>
				      <msqrt>
				        <mn>3</mn>
				      </msqrt>
				      <mspace width="thinmathspace" />
				      <mspace width="thinmathspace" />
				      <msub>
				        <mi>&#x03B3;<!-- γ --></mi>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>m0</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				  <mo>&gt;</mo>
				  <mtext>Shear force acting on web</mtext>
				</math>

				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>V</mi>
						    <mtext>p</mtext>
						  </msub>
						</math> = Shear yielding capacity <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						<msub>
						    <mi>A</mi>
						    <mtext>v</mtext>
						  </msub>
						</math> = Total cross-section area in shear  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>	
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						<msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m0</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor for failure  by yielding  <br> <br>

	&emsp; <b> <strong> ii. Shear rupture </strong></b>  [Reference: Clause 8.4.1, IS 800:2007, fin plate connection documentation] <br>
					<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>R</mi>
				    </mrow>
				    <mtext>n</mtext>
				  </msub>
				  <mo>=</mo>
				  <mn>0.6</mn>
				  <mspace width="thinmathspace" />
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>f</mi>
				    </mrow>
				    <mtext>u</mtext>
				  </msub>
				  <mspace width="thinmathspace" />
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>A</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>vn</mtext>
				    </mrow>
				  </msub>
				  <mo>&gt;</mo>
				  <mtext>shear force acting on the web</mtext>
				</math>

				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>R</mi>
						    <mtext>n</mtext>
						  </msub>
						</math> = Shear rupture capacity <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						<msub>
						    <mi>f</mi>
						    <mtext>u</mtext>
						  </msub>
						</math> = Characteristic ultimate shear stress  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mtext>vn</mtext>
						  </msub>
						</math> = Net area of the total cross-section in shear = <math xmlns="http://www.w3.org/1998/Math/MathML">


  <mo stretchy="false">(</mo>
  <msub>
    <mrow class="MJX-TeXAtom-ORD">
      <mi>b</mi>
      <mo>&#x2212;<!-- − --></mo>
      <mi>n</mi>
      <mspace width="thinmathspace" />
      <mi>d</mi>
    </mrow>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>h</mtext>
    </mrow>
  </msub>
  <mo stretchy="false">)</mo>
  <mspace width="thinmathspace" />
  <mrow class="MJX-TeXAtom-ORD">
    <mi>t</mi>
  </mrow>
</math> <br>

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>b</mi>
						</math> = Width of web splice plate in shear  <br>
						&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>n</mi>
						</math> =  Number of bolt holes in web splice plate  <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						<msub>
						    <mi>d</mi>
						    <mtext>h</mtext>
						  </msub>
						</math> = Diameter of bolt hole <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					<math xmlns="http://www.w3.org/1998/Math/MathML">
						    <mi>t</mi>
						</math> = Thickness of web splice plate  <br>	
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step20_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step20-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step20_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step20_feedback');
	$query->condition('uid', $user->uid);
	$form_step20_data = $query->execute();
	if ($form_step20_data)
	{
		if ($step20_data = $form_step20_data->fetchObject())
		{
			$form['step20_field1_fieldset']['step20_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step20_field1_fieldset']['step20_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step20_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step20_field1_fieldset']['step20_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step20_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step20_field1_fieldset\\[step20_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step20_data->id, $step20_data->data_relation);
			$icom = 1;
			$form['step20_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step20_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step20_num_comment']))
			{
				$form_state['step20_num_comment'] = 1;
			} //empty($form_state['step20_num_comment'])
			$step20_temp1 = 0;
			for ($step20_i = 0; $step20_i < $form_state['step20_num_comment']; $step20_i++)
			{
				$step20_temp1 = $step20_i;
				$form['step20_field1_fieldset'][$step20_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step20_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step20_field1_fieldset']["step20_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step20_temp1
			);
			$form['step20_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step20_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step20_comment_add_more_callback',
					'wrapper' => 'step20-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step20_num_comment'] > 1)
			{
				$form['step20_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step20_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step20_comment_add_more_callback',
						'wrapper' => 'step20-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step20_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step20_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step20_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step20_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step20_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step20_form_next_submit'
				)
			);
		} //$step20_data = $form_step20_data->fetchObject()
		else
		{
			$form['step20_field1_fieldset']['step20_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step20_field1_fieldset']['step20_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step20_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step20_field1_fieldset']['step20_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step20_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step20_field1_fieldset\\[step20_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step20_num_comment']))
			{
				$form_state['step20_num_comment'] = 1;
			} //empty($form_state['step20_num_comment'])
			$step20_temp1 = 0;
			for ($step20_i = 0; $step20_i < $form_state['step20_num_comment']; $step20_i++)
			{
				$step20_temp1 = $step20_i;
				$form['step20_field1_fieldset'][$step20_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step20_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step20_field1_fieldset']["step20_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step20_temp1
			);
			$form['step20_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step20_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step20_comment_add_more_callback',
					'wrapper' => 'step20-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step20_num_comment'] > 1)
			{
				$form['step20_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step20_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step20_comment_add_more_callback',
						'wrapper' => 'step20-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step20_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step20_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step20_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step20_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step20_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step20_form_next_submit'
				)
			);
		} //$step20_data = $form_step20_data->fetchObject()
	} //$form_step20_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step20_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step20_field1_fieldset']['step20_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step20_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step20_feedback');
	$query->condition('uid', $user->uid);
	$form_step20_data = $query->execute()->fetchObject();
	//var_dump($form_step20_data);die;
	if ($form_step20_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step20_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step20_field1_fieldset']['step20_field1_question1'],
			":question_ok_not_ok" => $v['step20_field1_fieldset']['step20_field1_question_ok'],
			":question_not_ok_comment" => $v['step20_field1_fieldset']['step20_field1_question_not_ok_comment'],
			":data_relation" => "step20"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step20_data->id
		));
		$form_step20_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++)
		{
			if ($v['step20_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step20_data->id,
					":number" => $i + $form_step20_comment_data->max + 1,
					":comment" => $v['step20_field1_fieldset'][$i]["comment"],
					":data_relation" => "step20",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step20_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++
	} //$form_step20_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step20_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step20_field1_fieldset']['step20_field1_question1'],
			":question_ok_not_ok" => $v['step20_field1_fieldset']['step20_field1_question_ok'],
			":question_not_ok_comment" => $v['step20_field1_fieldset']['step20_field1_question_not_ok_comment'],
			":data_relation" => "step20",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++)
		{
			if ($v['step20_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step20_field1_fieldset'][$i]["comment"],
					":data_relation" => "step20",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step20_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step19/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step20_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step20_field1_fieldset']['step20_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step20_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step20_feedback');
	$query->condition('uid', $user->uid);
	$form_step20_data = $query->execute()->fetchObject();
	//var_dump($form_step20_data);die;
	if ($form_step20_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step20_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step20_field1_fieldset']['step20_field1_question1'],
			":question_ok_not_ok" => $v['step20_field1_fieldset']['step20_field1_question_ok'],
			":question_not_ok_comment" => $v['step20_field1_fieldset']['step20_field1_question_not_ok_comment'],
			":data_relation" => "step20"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step20_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++)
		{
			if ($v['step20_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step20_data->id,
					":number" => $i + $form_step20_comment_data->max + 1,
					":comment" => $v['step20_field1_fieldset'][$i]["comment"],
					":data_relation" => "step20",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step20_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++
	} //$form_step20_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step20_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step20_field1_fieldset']['step20_field1_question1'],
			":question_ok_not_ok" => $v['step20_field1_fieldset']['step20_field1_question_ok'],
			":question_not_ok_comment" => $v['step20_field1_fieldset']['step20_field1_question_not_ok_comment'],
			":data_relation" => "step20",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++)
		{
			if ($v['step20_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step20_field1_fieldset'][$i]["comment"],
					":data_relation" => "step20",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step20_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step20_field1_fieldset']["step20_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step21/' . $user->uid;
}
/***************************************/
function step20_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step20_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step20_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step20_num_comment'] > 1)
	{
		$form_state['step20_num_comment']--;
	} //$form_state['step20_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step20_comment_add_more_callback($form, &$form_state)
{
	return $form['step20_field1_fieldset'];
}
/***************************************/
/***************************************** step 20 form ends ****************************/
/************************ Step 21 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step21_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('j. Web splice plate check > iii. Block shear capacity'));
	$img_path = '';
	$markup_text = '
	<b> <strong> j. Web splice plate checks </strong></b> <br>
	&emsp; <b> <strong> iii. Block shear capacity </strong></b>  [Reference: Clause 6.4.1 page 33, IS 800 : 2007] <br>
		&emsp;&emsp;			Block shear capacity of the plate should be greater than the factored applied shear force.

	
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <msub>
    <mrow class="MJX-TeXAtom-ORD">
      <mi>T</mi>
    </mrow>
    <mrow class="MJX-TeXAtom-ORD">
      <mtext>db</mtext>
    </mrow>
  </msub>
  <mo>&gt;</mo>
  <mtext>Factored shear force</mtext>
</math>

<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mtext>min</mtext>
				  <mspace width="thinmathspace" />
				  <mo stretchy="false">(</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db1</mtext>
				    </mrow>
				  </msub>
				  <mo>,</mo>
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db2</mtext>
				    </mrow>
				  </msub>
				  <mo stretchy="false">)</mo>
				</math> <br>

				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db1</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>vg</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>y</mtext>
				      </msub>
				    </mrow>
				    <mrow>
				      <msqrt>
				        <mn>3</mn>
				      </msqrt>
				      <mspace width="thinmathspace" />
				      <mspace width="thinmathspace" />
				      <msub>
				        <mi>&#x03B3;<!-- γ --></mi>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>m0</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				  <mo>+</mo>
				  <mfrac>
				    <mrow>
				      <mn>0.9</mn>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>tn</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>u</mtext>
				      </msub>
				    </mrow>
				    <msub>
				      <mi>&#x03B3;<!-- γ --></mi>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mtext>m1</mtext>
				      </mrow>
				    </msub>
				  </mfrac>
				</math> <br>

				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mi>T</mi>
				    </mrow>
				    <mrow class="MJX-TeXAtom-ORD">
				      <mtext>db2</mtext>
				    </mrow>
				  </msub>
				  <mo>=</mo>
				  <mfrac>
				    <mrow>
				      <mn>0.9</mn>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>vn</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>u</mtext>
				      </msub>
				    </mrow>
				    <mrow>
				      <msqrt>
				        <mn>3</mn>
				      </msqrt>
				      <mspace width="thinmathspace" />
				      <mspace width="thinmathspace" />
				      <msub>
				        <mi>&#x03B3;<!-- γ --></mi>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>m1</mtext>
				        </mrow>
				      </msub>
				    </mrow>
				  </mfrac>
				  <mo>+</mo>
				  <mfrac>
				    <mrow>
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>A</mi>
				        </mrow>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mtext>tg</mtext>
				        </mrow>
				      </msub>
				      <mspace width="thinmathspace" />
				      <msub>
				        <mrow class="MJX-TeXAtom-ORD">
				          <mi>f</mi>
				        </mrow>
				        <mtext>y</mtext>
				      </msub>
				    </mrow>
				    <msub>
				      <mi>&#x03B3;<!-- γ --></mi>
				      <mrow class="MJX-TeXAtom-ORD">
				        <mtext>m0</mtext>
				      </mrow>
				    </msub>
				  </mfrac>
				</math>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
					Where, <br>
					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>vg</mtext>
						    </mrow>
						  </msub>
						  <mo>,</mo>
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>vn</mtext>
						    </mrow>
						  </msub>
						</math> = minimum gross and net area in shear along bolt line parallel to external force respectively <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>tg</mtext>
						    </mrow>
						  </msub>
						  <mo>,</mo>
						  <msub>
						    <mi>A</mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>tn</mtext>
						    </mrow>
						  </msub>
						</math> = minimum gross and net area in tension from the bolt hole to the toe, end bolt line, perpendicular to the line of force <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>y</mtext>
						  </msub>
						</math> = Characteristic yield stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>f</mi>
						    <mtext>u</mtext>
						  </msub>
						</math> = Characteristic ultimate tensile stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m1</mtext>
						    </mrow>
						  </msub>
						</math> = partial safety factor for failure at ultimate stress <br>

					&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
						<math xmlns="http://www.w3.org/1998/Math/MathML">
						  <msub>
						    <mi>&#x03B3;<!-- γ --></mi>
						    <mrow class="MJX-TeXAtom-ORD">
						      <mtext>m0</mtext>
						    </mrow>
						  </msub>
						</math> = Partial safety factor for failure in tension by yielding <br>

 &emsp;&emsp; <strong> This step is same as implemented in shear connection modules (already reviewed) </strong>

	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step21_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step21-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step21_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step21_feedback');
	$query->condition('uid', $user->uid);
	$form_step21_data = $query->execute();
	if ($form_step21_data)
	{
		if ($step21_data = $form_step21_data->fetchObject())
		{
			$form['step21_field1_fieldset']['step21_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step21_field1_fieldset']['step21_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step21_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step21_field1_fieldset']['step21_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step21_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step21_field1_fieldset\\[step21_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step21_data->id, $step21_data->data_relation);
			$icom = 1;
			$form['step21_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step21_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step21_num_comment']))
			{
				$form_state['step21_num_comment'] = 1;
			} //empty($form_state['step21_num_comment'])
			$step21_temp1 = 0;
			for ($step21_i = 0; $step21_i < $form_state['step21_num_comment']; $step21_i++)
			{
				$step21_temp1 = $step21_i;
				$form['step21_field1_fieldset'][$step21_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step21_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step21_field1_fieldset']["step21_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step21_temp1
			);
			$form['step21_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step21_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step21_comment_add_more_callback',
					'wrapper' => 'step21-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step21_num_comment'] > 1)
			{
				$form['step21_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step21_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step21_comment_add_more_callback',
						'wrapper' => 'step21-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step21_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step21_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step21_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step21_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step21_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step21_form_next_submit'
				)
			);
		} //$step21_data = $form_step21_data->fetchObject()
		else
		{
			$form['step21_field1_fieldset']['step21_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step21_field1_fieldset']['step21_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step21_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step21_field1_fieldset']['step21_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step21_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step21_field1_fieldset\\[step21_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step21_num_comment']))
			{
				$form_state['step21_num_comment'] = 1;
			} //empty($form_state['step21_num_comment'])
			$step21_temp1 = 0;
			for ($step21_i = 0; $step21_i < $form_state['step21_num_comment']; $step21_i++)
			{
				$step21_temp1 = $step21_i;
				$form['step21_field1_fieldset'][$step21_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step21_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step21_field1_fieldset']["step21_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step21_temp1
			);
			$form['step21_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step21_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step21_comment_add_more_callback',
					'wrapper' => 'step21-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step21_num_comment'] > 1)
			{
				$form['step21_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step21_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step21_comment_add_more_callback',
						'wrapper' => 'step21-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step21_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step21_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step21_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step21_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step21_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step21_form_next_submit'
				)
			);
		} //$step21_data = $form_step21_data->fetchObject()
	} //$form_step21_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step21_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step21_field1_fieldset']['step21_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step21_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step21_feedback');
	$query->condition('uid', $user->uid);
	$form_step21_data = $query->execute()->fetchObject();
	//var_dump($form_step21_data);die;
	if ($form_step21_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step21_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step21_field1_fieldset']['step21_field1_question1'],
			":question_ok_not_ok" => $v['step21_field1_fieldset']['step21_field1_question_ok'],
			":question_not_ok_comment" => $v['step21_field1_fieldset']['step21_field1_question_not_ok_comment'],
			":data_relation" => "step21"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step21_data->id
		));
		$form_step21_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++)
		{
			if ($v['step21_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step21_data->id,
					":number" => $i + $form_step21_comment_data->max + 1,
					":comment" => $v['step21_field1_fieldset'][$i]["comment"],
					":data_relation" => "step21",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step21_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++
	} //$form_step21_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step21_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step21_field1_fieldset']['step21_field1_question1'],
			":question_ok_not_ok" => $v['step21_field1_fieldset']['step21_field1_question_ok'],
			":question_not_ok_comment" => $v['step21_field1_fieldset']['step21_field1_question_not_ok_comment'],
			":data_relation" => "step21",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++)
		{
			if ($v['step21_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step21_field1_fieldset'][$i]["comment"],
					":data_relation" => "step21",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step21_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step20/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step21_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step21_field1_fieldset']['step21_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step21_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step21_feedback');
	$query->condition('uid', $user->uid);
	$form_step21_data = $query->execute()->fetchObject();
	//var_dump($form_step21_data);die;
	if ($form_step21_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step21_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step21_field1_fieldset']['step21_field1_question1'],
			":question_ok_not_ok" => $v['step21_field1_fieldset']['step21_field1_question_ok'],
			":question_not_ok_comment" => $v['step21_field1_fieldset']['step21_field1_question_not_ok_comment'],
			":data_relation" => "step21"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step21_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++)
		{
			if ($v['step21_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step21_data->id,
					":number" => $i + $form_step21_comment_data->max + 1,
					":comment" => $v['step21_field1_fieldset'][$i]["comment"],
					":data_relation" => "step21",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step21_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++
	} //$form_step21_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step21_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step21_field1_fieldset']['step21_field1_question1'],
			":question_ok_not_ok" => $v['step21_field1_fieldset']['step21_field1_question_ok'],
			":question_not_ok_comment" => $v['step21_field1_fieldset']['step21_field1_question_not_ok_comment'],
			":data_relation" => "step21",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++)
		{
			if ($v['step21_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step21_field1_fieldset'][$i]["comment"],
					":data_relation" => "step21",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step21_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step21_field1_fieldset']["step21_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step22/' . $user->uid;
}
/***************************************/
function step21_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step21_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step21_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step21_num_comment'] > 1)
	{
		$form_state['step21_num_comment']--;
	} //$form_state['step21_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step21_comment_add_more_callback($form, &$form_state)
{
	return $form['step21_field1_fieldset'];
}
/***************************************/
/***************************************** step 21 form ends ****************************/

/************************ Step 22 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step22_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Thank you'));
	$img_path = $base_url . '/' . drupal_get_path("module", "osdag_response_form") . '/images';
	$markup_text = '
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;				
				<img src="' . $img_path . '/ThankYou.jpg" width="70%" height="70%" align="middle" />
				<br><br>
				&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
				
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step22_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step22-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step22_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step22_feedback');
	$query->condition('uid', $user->uid);
	$form_step22_data = $query->execute();
	if ($form_step22_data)
	{
		if ($step22_data = $form_step22_data->fetchObject())
		{
			$form['step22_field1_fieldset']['step22_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step22_field1_fieldset']['step22_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step22_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step22_field1_fieldset']['step22_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step22_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step22_field1_fieldset\\[step22_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step22_data->id, $step22_data->data_relation);
			$icom = 1;
			$form['step22_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step22_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step22_num_comment']))
			{
				$form_state['step22_num_comment'] = 1;
			} //empty($form_state['step22_num_comment'])
			$step22_temp1 = 0;
			for ($step22_i = 0; $step22_i < $form_state['step22_num_comment']; $step22_i++)
			{
				$step22_temp1 = $step22_i;
				$form['step22_field1_fieldset'][$step22_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step22_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step22_field1_fieldset']["step22_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step22_temp1
			);
			$form['step22_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step22_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step22_comment_add_more_callback',
					'wrapper' => 'step22-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step22_num_comment'] > 1)
			{
				$form['step22_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step22_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step22_comment_add_more_callback',
						'wrapper' => 'step22-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step22_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step22_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step22_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step22_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step22_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step22_form_next_submit'
				)
			);
		} //$step22_data = $form_step22_data->fetchObject()
		else
		{
			$form['step22_field1_fieldset']['step22_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step22_field1_fieldset']['step22_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step22_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step22_field1_fieldset']['step22_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step22_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step22_field1_fieldset\\[step22_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step22_num_comment']))
			{
				$form_state['step22_num_comment'] = 1;
			} //empty($form_state['step22_num_comment'])
			$step22_temp1 = 0;
			for ($step22_i = 0; $step22_i < $form_state['step22_num_comment']; $step22_i++)
			{
				$step22_temp1 = $step22_i;
				$form['step22_field1_fieldset'][$step22_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step22_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step22_field1_fieldset']["step22_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step22_temp1
			);
			$form['step22_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step22_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step22_comment_add_more_callback',
					'wrapper' => 'step22-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step22_num_comment'] > 1)
			{
				$form['step22_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step22_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step22_comment_add_more_callback',
						'wrapper' => 'step22-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step22_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step22_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step22_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step22_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step22_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step22_form_next_submit'
				)
			);
		} //$step22_data = $form_step22_data->fetchObject()
	} //$form_step22_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step22_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step22_field1_fieldset']['step22_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step22_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step22_feedback');
	$query->condition('uid', $user->uid);
	$form_step22_data = $query->execute()->fetchObject();
	//var_dump($form_step22_data);die;
	if ($form_step22_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step22_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step22_field1_fieldset']['step22_field1_question1'],
			":question_ok_not_ok" => $v['step22_field1_fieldset']['step22_field1_question_ok'],
			":question_not_ok_comment" => $v['step22_field1_fieldset']['step22_field1_question_not_ok_comment'],
			":data_relation" => "step22"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step22_data->id
		));
		$form_step22_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++)
		{
			if ($v['step22_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step22_data->id,
					":number" => $i + $form_step22_comment_data->max + 1,
					":comment" => $v['step22_field1_fieldset'][$i]["comment"],
					":data_relation" => "step22",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step22_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++
	} //$form_step22_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step22_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step22_field1_fieldset']['step22_field1_question1'],
			":question_ok_not_ok" => $v['step22_field1_fieldset']['step22_field1_question_ok'],
			":question_not_ok_comment" => $v['step22_field1_fieldset']['step22_field1_question_not_ok_comment'],
			":data_relation" => "step22",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++)
		{
			if ($v['step22_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step22_field1_fieldset'][$i]["comment"],
					":data_relation" => "step22",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step22_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step21/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step22_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step22_field1_fieldset']['step22_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step22_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step22_feedback');
	$query->condition('uid', $user->uid);
	$form_step22_data = $query->execute()->fetchObject();
	//var_dump($form_step22_data);die;
	if ($form_step22_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step22_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step22_field1_fieldset']['step22_field1_question1'],
			":question_ok_not_ok" => $v['step22_field1_fieldset']['step22_field1_question_ok'],
			":question_not_ok_comment" => $v['step22_field1_fieldset']['step22_field1_question_not_ok_comment'],
			":data_relation" => "step22"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step22_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++)
		{
			if ($v['step22_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step22_data->id,
					":number" => $i + $form_step22_comment_data->max + 1,
					":comment" => $v['step22_field1_fieldset'][$i]["comment"],
					":data_relation" => "step22",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step22_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++
	} //$form_step22_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step22_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step22_field1_fieldset']['step22_field1_question1'],
			":question_ok_not_ok" => $v['step22_field1_fieldset']['step22_field1_question_ok'],
			":question_not_ok_comment" => $v['step22_field1_fieldset']['step22_field1_question_not_ok_comment'],
			":data_relation" => "step22",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++)
		{
			if ($v['step22_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step22_field1_fieldset'][$i]["comment"],
					":data_relation" => "step22",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step22_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step22_field1_fieldset']["step22_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step23/' . $user->uid;
}
/***************************************/
function step22_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step22_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step22_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step22_num_comment'] > 1)
	{
		$form_state['step22_num_comment']--;
	} //$form_state['step22_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step22_comment_add_more_callback($form, &$form_state)
{
	return $form['step22_field1_fieldset'];
}
/***************************************/
/***************************************** step 22 form ends ****************************/

/************************ Step 23 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step23_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('d. Detailing checks > ii. Edge and end distances'));
	$img_path = '';
	$markup_text = '
	<b> d. Detailing checks </b> <br>
	&emsp; <b> ii. Edge and end distances </b> [Cl 10.2.4] <br>
	&emsp;&emsp;&emsp; [Cl 10.2.4.2] <br>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; The minimum edge and end distances from the centre of any hole to the nearest edge of the column/end plate shall not be less than 1.7 times the hole diameter in case of sheared or hand-flame cut edges; and 1.5 times the hole diameter in case of rolled, machine-flame cut, sawn and planed edges. <br>
				
						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>1</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>

						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>2</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>
	
	&emsp;&emsp;&emsp; [Cl 10.2.4.3] <br>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; The maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part should not exceed 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mn>12</mn>
		  <mi>t</mi>
		  <mi>&#x03F5;<!-- ϵ --></mi>
		</math>
	, where
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>&#x03F5;<!-- ϵ --></mi>
		  <mo>=</mo>
		  <msqrt>
			<mn>250</mn>
			<mrow class="MJX-TeXAtom-ORD">
			  <mo>/</mo>
			</mrow>
			<msub>
			  <mi>f</mi>
			  <mi>y</mi>
			</msub>
		  </msqrt>
		</math>
	and 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>t</mi>
		</math>
	is the thickness of the thinner component.  <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
					<mi>e</mi>
					<mn>2</mn>
				  </msub>
				  <mo>&#x2264;</mo>
				  <mn>12</mn>
				  <mi>t</mi>
				  <mi>&#x03F5;<!-- ϵ --></mi>
				</math>
			
		&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
		Where, <br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>1</mn>
			  </msub>
			</math>
			- End distance <br>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>2</mn>
			  </msub>
			</math>
			- Edge distance <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>d</mi>
				<mn>h</mn>
			  </msub>
			</math> 
			- Diameter of bolt hole <br>
			
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <mi>&#x03F5;<!-- ϵ --></mi>
			  <mo>=</mo>
			  <msqrt>
				<mn>250</mn>
				<mrow class="MJX-TeXAtom-ORD">
				  <mo>/</mo>
				</mrow>
				<msub>
				  <mi>f</mi>
				  <mi>y</mi>
				</msub>
			  </msqrt>
			</math> <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>f</mi>
				<mn>y</mn>
			  </msub>
			</math>
			- yield strength of end plate <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
				<mi>t</mi>
			</math> 
			- thickness of the thinner component 
			<br>
			<br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Note: Where the members are exposed to corrosive influences, the maximum edge distance shall not exceed 40 mm plus 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mn>4</mn>
					<mi>t</mi>
			</math> 
			, where 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mi>t</mi>
			</math> 
			is the thickness of thinner connected plate.
	
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step23_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step23-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step23_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step23_feedback');
	$query->condition('uid', $user->uid);
	$form_step23_data = $query->execute();
	if ($form_step23_data)
	{
		if ($step23_data = $form_step23_data->fetchObject())
		{
			$form['step23_field1_fieldset']['step23_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step23_field1_fieldset']['step23_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step23_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step23_field1_fieldset']['step23_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step23_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step23_field1_fieldset\\[step23_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step23_data->id, $step23_data->data_relation);
			$icom = 1;
			$form['step23_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step23_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step23_num_comment']))
			{
				$form_state['step23_num_comment'] = 1;
			} //empty($form_state['step23_num_comment'])
			$step23_temp1 = 0;
			for ($step23_i = 0; $step23_i < $form_state['step23_num_comment']; $step23_i++)
			{
				$step23_temp1 = $step23_i;
				$form['step23_field1_fieldset'][$step23_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step23_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step23_field1_fieldset']["step23_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step23_temp1
			);
			$form['step23_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step23_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step23_comment_add_more_callback',
					'wrapper' => 'step23-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step23_num_comment'] > 1)
			{
				$form['step23_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step23_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step23_comment_add_more_callback',
						'wrapper' => 'step23-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step23_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step23_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step23_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step23_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step23_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step23_form_next_submit'
				)
			);
		} //$step23_data = $form_step23_data->fetchObject()
		else
		{
			$form['step23_field1_fieldset']['step23_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step23_field1_fieldset']['step23_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step23_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step23_field1_fieldset']['step23_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step23_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step23_field1_fieldset\\[step23_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step23_num_comment']))
			{
				$form_state['step23_num_comment'] = 1;
			} //empty($form_state['step23_num_comment'])
			$step23_temp1 = 0;
			for ($step23_i = 0; $step23_i < $form_state['step23_num_comment']; $step23_i++)
			{
				$step23_temp1 = $step23_i;
				$form['step23_field1_fieldset'][$step23_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step23_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step23_field1_fieldset']["step23_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step23_temp1
			);
			$form['step23_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step23_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step23_comment_add_more_callback',
					'wrapper' => 'step23-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step23_num_comment'] > 1)
			{
				$form['step23_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step23_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step23_comment_add_more_callback',
						'wrapper' => 'step23-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step23_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step23_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step23_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step23_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step23_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step23_form_next_submit'
				)
			);
		} //$step23_data = $form_step23_data->fetchObject()
	} //$form_step23_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step23_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step23_field1_fieldset']['step23_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step23_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step23_feedback');
	$query->condition('uid', $user->uid);
	$form_step23_data = $query->execute()->fetchObject();
	//var_dump($form_step23_data);die;
	if ($form_step23_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step23_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step23_field1_fieldset']['step23_field1_question1'],
			":question_ok_not_ok" => $v['step23_field1_fieldset']['step23_field1_question_ok'],
			":question_not_ok_comment" => $v['step23_field1_fieldset']['step23_field1_question_not_ok_comment'],
			":data_relation" => "step23"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step23_data->id
		));
		$form_step23_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++)
		{
			if ($v['step23_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step23_data->id,
					":number" => $i + $form_step23_comment_data->max + 1,
					":comment" => $v['step23_field1_fieldset'][$i]["comment"],
					":data_relation" => "step23",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step23_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++
	} //$form_step23_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step23_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step23_field1_fieldset']['step23_field1_question1'],
			":question_ok_not_ok" => $v['step23_field1_fieldset']['step23_field1_question_ok'],
			":question_not_ok_comment" => $v['step23_field1_fieldset']['step23_field1_question_not_ok_comment'],
			":data_relation" => "step23",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++)
		{
			if ($v['step23_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step23_field1_fieldset'][$i]["comment"],
					":data_relation" => "step23",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step23_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step22/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step23_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step23_field1_fieldset']['step23_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step23_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step23_feedback');
	$query->condition('uid', $user->uid);
	$form_step23_data = $query->execute()->fetchObject();
	//var_dump($form_step23_data);die;
	if ($form_step23_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step23_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step23_field1_fieldset']['step23_field1_question1'],
			":question_ok_not_ok" => $v['step23_field1_fieldset']['step23_field1_question_ok'],
			":question_not_ok_comment" => $v['step23_field1_fieldset']['step23_field1_question_not_ok_comment'],
			":data_relation" => "step23"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step23_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++)
		{
			if ($v['step23_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step23_data->id,
					":number" => $i + $form_step23_comment_data->max + 1,
					":comment" => $v['step23_field1_fieldset'][$i]["comment"],
					":data_relation" => "step23",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step23_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++
	} //$form_step23_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step23_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step23_field1_fieldset']['step23_field1_question1'],
			":question_ok_not_ok" => $v['step23_field1_fieldset']['step23_field1_question_ok'],
			":question_not_ok_comment" => $v['step23_field1_fieldset']['step23_field1_question_not_ok_comment'],
			":data_relation" => "step23",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++)
		{
			if ($v['step23_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step23_field1_fieldset'][$i]["comment"],
					":data_relation" => "step23",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step23_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step23_field1_fieldset']["step23_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step24/' . $user->uid;
}
/***************************************/
function step23_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step23_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step23_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step23_num_comment'] > 1)
	{
		$form_state['step23_num_comment']--;
	} //$form_state['step23_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step23_comment_add_more_callback($form, &$form_state)
{
	return $form['step23_field1_fieldset'];
}
/***************************************/
/***************************************** step 23 form ends ****************************/

/************************ Step 24 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step24_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('d. Detailing checks > ii. Edge and end distances'));
	$img_path = '';
	$markup_text = '
	<b> d. Detailing checks </b> <br>
	&emsp; <b> ii. Edge and end distances </b> [Cl 10.2.4] <br>
	&emsp;&emsp;&emsp; [Cl 10.2.4.2] <br>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; The minimum edge and end distances from the centre of any hole to the nearest edge of the column/end plate shall not be less than 1.7 times the hole diameter in case of sheared or hand-flame cut edges; and 1.5 times the hole diameter in case of rolled, machine-flame cut, sawn and planed edges. <br>
				
						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>1</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>

						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>2</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>
	
	&emsp;&emsp;&emsp; [Cl 10.2.4.3] <br>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; The maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part should not exceed 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mn>12</mn>
		  <mi>t</mi>
		  <mi>&#x03F5;<!-- ϵ --></mi>
		</math>
	, where
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>&#x03F5;<!-- ϵ --></mi>
		  <mo>=</mo>
		  <msqrt>
			<mn>250</mn>
			<mrow class="MJX-TeXAtom-ORD">
			  <mo>/</mo>
			</mrow>
			<msub>
			  <mi>f</mi>
			  <mi>y</mi>
			</msub>
		  </msqrt>
		</math>
	and 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>t</mi>
		</math>
	is the thickness of the thinner component.  <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
					<mi>e</mi>
					<mn>2</mn>
				  </msub>
				  <mo>&#x2264;</mo>
				  <mn>12</mn>
				  <mi>t</mi>
				  <mi>&#x03F5;<!-- ϵ --></mi>
				</math>
			
		&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
		Where, <br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>1</mn>
			  </msub>
			</math>
			- End distance <br>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>2</mn>
			  </msub>
			</math>
			- Edge distance <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>d</mi>
				<mn>h</mn>
			  </msub>
			</math> 
			- Diameter of bolt hole <br>
			
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <mi>&#x03F5;<!-- ϵ --></mi>
			  <mo>=</mo>
			  <msqrt>
				<mn>250</mn>
				<mrow class="MJX-TeXAtom-ORD">
				  <mo>/</mo>
				</mrow>
				<msub>
				  <mi>f</mi>
				  <mi>y</mi>
				</msub>
			  </msqrt>
			</math> <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>f</mi>
				<mn>y</mn>
			  </msub>
			</math>
			- yield strength of end plate <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
				<mi>t</mi>
			</math> 
			- thickness of the thinner component 
			<br>
			<br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Note: Where the members are exposed to corrosive influences, the maximum edge distance shall not exceed 40 mm plus 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mn>4</mn>
					<mi>t</mi>
			</math> 
			, where 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mi>t</mi>
			</math> 
			is the thickness of thinner connected plate.
	
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step24_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step24-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step24_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step24_feedback');
	$query->condition('uid', $user->uid);
	$form_step24_data = $query->execute();
	if ($form_step24_data)
	{
		if ($step24_data = $form_step24_data->fetchObject())
		{
			$form['step24_field1_fieldset']['step24_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step24_field1_fieldset']['step24_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step24_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step24_field1_fieldset']['step24_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step24_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step24_field1_fieldset\\[step24_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step24_data->id, $step24_data->data_relation);
			$icom = 1;
			$form['step24_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step24_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step24_num_comment']))
			{
				$form_state['step24_num_comment'] = 1;
			} //empty($form_state['step24_num_comment'])
			$step24_temp1 = 0;
			for ($step24_i = 0; $step24_i < $form_state['step24_num_comment']; $step24_i++)
			{
				$step24_temp1 = $step24_i;
				$form['step24_field1_fieldset'][$step24_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step24_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step24_field1_fieldset']["step24_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step24_temp1
			);
			$form['step24_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step24_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step24_comment_add_more_callback',
					'wrapper' => 'step24-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step24_num_comment'] > 1)
			{
				$form['step24_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step24_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step24_comment_add_more_callback',
						'wrapper' => 'step24-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step24_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step24_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step24_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step24_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step24_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step24_form_next_submit'
				)
			);
		} //$step24_data = $form_step24_data->fetchObject()
		else
		{
			$form['step24_field1_fieldset']['step24_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step24_field1_fieldset']['step24_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step24_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step24_field1_fieldset']['step24_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step24_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step24_field1_fieldset\\[step24_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step24_num_comment']))
			{
				$form_state['step24_num_comment'] = 1;
			} //empty($form_state['step24_num_comment'])
			$step24_temp1 = 0;
			for ($step24_i = 0; $step24_i < $form_state['step24_num_comment']; $step24_i++)
			{
				$step24_temp1 = $step24_i;
				$form['step24_field1_fieldset'][$step24_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step24_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step24_field1_fieldset']["step24_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step24_temp1
			);
			$form['step24_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step24_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step24_comment_add_more_callback',
					'wrapper' => 'step24-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step24_num_comment'] > 1)
			{
				$form['step24_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step24_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step24_comment_add_more_callback',
						'wrapper' => 'step24-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step24_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step24_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step24_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step24_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step24_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step24_form_next_submit'
				)
			);
		} //$step24_data = $form_step24_data->fetchObject()
	} //$form_step24_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step24_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step24_field1_fieldset']['step24_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step24_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step24_feedback');
	$query->condition('uid', $user->uid);
	$form_step24_data = $query->execute()->fetchObject();
	//var_dump($form_step24_data);die;
	if ($form_step24_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step24_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step24_field1_fieldset']['step24_field1_question1'],
			":question_ok_not_ok" => $v['step24_field1_fieldset']['step24_field1_question_ok'],
			":question_not_ok_comment" => $v['step24_field1_fieldset']['step24_field1_question_not_ok_comment'],
			":data_relation" => "step24"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step24_data->id
		));
		$form_step24_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++)
		{
			if ($v['step24_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step24_data->id,
					":number" => $i + $form_step24_comment_data->max + 1,
					":comment" => $v['step24_field1_fieldset'][$i]["comment"],
					":data_relation" => "step24",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step24_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++
	} //$form_step24_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step24_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step24_field1_fieldset']['step24_field1_question1'],
			":question_ok_not_ok" => $v['step24_field1_fieldset']['step24_field1_question_ok'],
			":question_not_ok_comment" => $v['step24_field1_fieldset']['step24_field1_question_not_ok_comment'],
			":data_relation" => "step24",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++)
		{
			if ($v['step24_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step24_field1_fieldset'][$i]["comment"],
					":data_relation" => "step24",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step24_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step23/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step24_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step24_field1_fieldset']['step24_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step24_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step24_feedback');
	$query->condition('uid', $user->uid);
	$form_step24_data = $query->execute()->fetchObject();
	//var_dump($form_step24_data);die;
	if ($form_step24_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step24_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step24_field1_fieldset']['step24_field1_question1'],
			":question_ok_not_ok" => $v['step24_field1_fieldset']['step24_field1_question_ok'],
			":question_not_ok_comment" => $v['step24_field1_fieldset']['step24_field1_question_not_ok_comment'],
			":data_relation" => "step24"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step24_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++)
		{
			if ($v['step24_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step24_data->id,
					":number" => $i + $form_step24_comment_data->max + 1,
					":comment" => $v['step24_field1_fieldset'][$i]["comment"],
					":data_relation" => "step24",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step24_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++
	} //$form_step24_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step24_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step24_field1_fieldset']['step24_field1_question1'],
			":question_ok_not_ok" => $v['step24_field1_fieldset']['step24_field1_question_ok'],
			":question_not_ok_comment" => $v['step24_field1_fieldset']['step24_field1_question_not_ok_comment'],
			":data_relation" => "step24",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++)
		{
			if ($v['step24_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step24_field1_fieldset'][$i]["comment"],
					":data_relation" => "step24",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step24_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step24_field1_fieldset']["step24_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step25/' . $user->uid;
}
/***************************************/
function step24_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step24_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step24_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step24_num_comment'] > 1)
	{
		$form_state['step24_num_comment']--;
	} //$form_state['step24_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step24_comment_add_more_callback($form, &$form_state)
{
	return $form['step24_field1_fieldset'];
}
/***************************************/
/***************************************** step 24 form ends ****************************/

/************************ Step 25 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step25_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('d. Detailing checks > ii. Edge and end distances'));
	$img_path = '';
	$markup_text = '
	<b> d. Detailing checks </b> <br>
	&emsp; <b> ii. Edge and end distances </b> [Cl 10.2.4] <br>
	&emsp;&emsp;&emsp; [Cl 10.2.4.2] <br>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; The minimum edge and end distances from the centre of any hole to the nearest edge of the column/end plate shall not be less than 1.7 times the hole diameter in case of sheared or hand-flame cut edges; and 1.5 times the hole diameter in case of rolled, machine-flame cut, sawn and planed edges. <br>
				
						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>1</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>

						<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
						  <msub>
							<mi>e</mi>
							<mn>2</mn>
						  </msub>
						  <mo>&#x2265;</mo>
						  <mn>1.5</mn>
						  <msub>
							<mi>d</mi>
							<mi>h</mi>
						  </msub>
						</math>
	
	&emsp;&emsp;&emsp; [Cl 10.2.4.3] <br>
	&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; The maximum edge distance to the nearest line of fasteners from an edge of any un-stiffened part should not exceed 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mn>12</mn>
		  <mi>t</mi>
		  <mi>&#x03F5;<!-- ϵ --></mi>
		</math>
	, where
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>&#x03F5;<!-- ϵ --></mi>
		  <mo>=</mo>
		  <msqrt>
			<mn>250</mn>
			<mrow class="MJX-TeXAtom-ORD">
			  <mo>/</mo>
			</mrow>
			<msub>
			  <mi>f</mi>
			  <mi>y</mi>
			</msub>
		  </msqrt>
		</math>
	and 
		<math xmlns="http://www.w3.org/1998/Math/MathML">
		  <mi>t</mi>
		</math>
	is the thickness of the thinner component.  <br>
				<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
				  <msub>
					<mi>e</mi>
					<mn>2</mn>
				  </msub>
				  <mo>&#x2264;</mo>
				  <mn>12</mn>
				  <mi>t</mi>
				  <mi>&#x03F5;<!-- ϵ --></mi>
				</math>
			
		&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
		Where, <br>
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>1</mn>
			  </msub>
			</math>
			- End distance <br>

			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>e</mi>
				<mn>2</mn>
			  </msub>
			</math>
			- Edge distance <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>d</mi>
				<mn>h</mn>
			  </msub>
			</math> 
			- Diameter of bolt hole <br>
			
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <mi>&#x03F5;<!-- ϵ --></mi>
			  <mo>=</mo>
			  <msqrt>
				<mn>250</mn>
				<mrow class="MJX-TeXAtom-ORD">
				  <mo>/</mo>
				</mrow>
				<msub>
				  <mi>f</mi>
				  <mi>y</mi>
				</msub>
			  </msqrt>
			</math> <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
			  <msub>
				<mi>f</mi>
				<mn>y</mn>
			  </msub>
			</math>
			- yield strength of end plate <br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			<math xmlns="http://www.w3.org/1998/Math/MathML">
				<mi>t</mi>
			</math> 
			- thickness of the thinner component 
			<br>
			<br>
			
			&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
			Note: Where the members are exposed to corrosive influences, the maximum edge distance shall not exceed 40 mm plus 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mn>4</mn>
					<mi>t</mi>
			</math> 
			, where 
			<math xmlns="http://www.w3.org/1998/Math/MathML">
					<mi>t</mi>
			</math> 
			is the thickness of thinner connected plate.
	
	
	<hr>';
	// All the real form fields.
	$form = array();
	$form['step25_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#tree' => TRUE,
		'#prefix' => '<div id="step25-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step25_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step25_feedback');
	$query->condition('uid', $user->uid);
	$form_step25_data = $query->execute();
	if ($form_step25_data)
	{
		if ($step25_data = $form_step25_data->fetchObject())
		{
			$form['step25_field1_fieldset']['step25_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step25_field1_fieldset']['step25_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				'#default_value' => $step25_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step25_field1_fieldset']['step25_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				'#default_value' => $step25_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step25_field1_fieldset\\[step25_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step25_data->id, $step25_data->data_relation);
			$icom = 1;
			$form['step25_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => 'Earlier comment<br>'
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step25_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step25_num_comment']))
			{
				$form_state['step25_num_comment'] = 1;
			} //empty($form_state['step25_num_comment'])
			$step25_temp1 = 0;
			for ($step25_i = 0; $step25_i < $form_state['step25_num_comment']; $step25_i++)
			{
				$step25_temp1 = $step25_i;
				$form['step25_field1_fieldset'][$step25_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step25_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step25_field1_fieldset']["step25_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step25_temp1
			);
			$form['step25_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step25_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step25_comment_add_more_callback',
					'wrapper' => 'step25-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step25_num_comment'] > 1)
			{
				$form['step25_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step25_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step25_comment_add_more_callback',
						'wrapper' => 'step25-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step25_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step25_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step25_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step25_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step25_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step25_form_next_submit'
				)
			);
		} //$step25_data = $form_step25_data->fetchObject()
		else
		{
			$form['step25_field1_fieldset']['step25_field1_question1'] = array(
				'#markup' => $markup_text
			);
			$form['step25_field1_fieldset']['step25_field1_question_ok'] = array(
				'#title' => '<strong>Is this ok/not ok</strong>',
				'#type' => 'radios',
				'#options' => array(
					'Ok' => 'Ok',
					'Not ok' => 'Not ok'
				),
				//'#default_value' => $step25_data->question_ok_not_ok,
				'#required' => true
			);
			$form['step25_field1_fieldset']['step25_field1_question_not_ok_comment'] = array(
				//'#title' => 'If not, ple?',
				'#type' => 'textarea',
				//'#default_value' => $step25_data->question_not_ok_comment,
				'#states' => array(
					'visible' => array(
						':input[name="step25_field1_fieldset\\[step25_field1_question_ok\\]"]' => array(
							array(
								'value' => t('Not ok')
							)
						)
					)
				)
			);
			if (empty($form_state['step25_num_comment']))
			{
				$form_state['step25_num_comment'] = 1;
			} //empty($form_state['step25_num_comment'])
			$step25_temp1 = 0;
			for ($step25_i = 0; $step25_i < $form_state['step25_num_comment']; $step25_i++)
			{
				$step25_temp1 = $step25_i;
				$form['step25_field1_fieldset'][$step25_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step25_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step25_field1_fieldset']["step25_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step25_temp1
			);
			$form['step25_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step25_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step25_comment_add_more_callback',
					'wrapper' => 'step25-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step25_num_comment'] > 1)
			{
				$form['step25_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step25_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step25_comment_add_more_callback',
						'wrapper' => 'step25-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step25_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step25_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step25_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step25_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form["step1_page_id"] = array(
				"#type" => "hidden",
				"#value" => "step1"
			);
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step25_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Save & Next',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step25_form_next_submit'
				)
			);
		} //$step25_data = $form_step25_data->fetchObject()
	} //$form_step25_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step25_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step25_field1_fieldset']['step25_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step25_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step25_feedback');
	$query->condition('uid', $user->uid);
	$form_step25_data = $query->execute()->fetchObject();
	//var_dump($form_step25_data);die;
	if ($form_step25_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step25_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step25_field1_fieldset']['step25_field1_question1'],
			":question_ok_not_ok" => $v['step25_field1_fieldset']['step25_field1_question_ok'],
			":question_not_ok_comment" => $v['step25_field1_fieldset']['step25_field1_question_not_ok_comment'],
			":data_relation" => "step25"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step25_data->id
		));
		$form_step25_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++)
		{
			if ($v['step25_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step25_data->id,
					":number" => $i + $form_step25_comment_data->max + 1,
					":comment" => $v['step25_field1_fieldset'][$i]["comment"],
					":data_relation" => "step25",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step25_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++
	} //$form_step25_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step25_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1,  :question_ok_not_ok, :question_not_ok_comment,:data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step25_field1_fieldset']['step25_field1_question1'],
			":question_ok_not_ok" => $v['step25_field1_fieldset']['step25_field1_question_ok'],
			":question_not_ok_comment" => $v['step25_field1_fieldset']['step25_field1_question_not_ok_comment'],
			":data_relation" => "step25",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++)
		{
			if ($v['step25_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step25_field1_fieldset'][$i]["comment"],
					":data_relation" => "step25",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step25_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step24/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step25_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step25_field1_fieldset']['step25_field1_question1'] = 'question 1';
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step25_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step25_feedback');
	$query->condition('uid', $user->uid);
	$form_step25_data = $query->execute()->fetchObject();
	//var_dump($form_step25_data);die;
	if ($form_step25_data)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step25_feedback SET question1=:question1, question_ok_not_ok=:question_ok_not_ok, question_not_ok_comment=:question_not_ok_comment, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step25_field1_fieldset']['step25_field1_question1'],
			":question_ok_not_ok" => $v['step25_field1_fieldset']['step25_field1_question_ok'],
			":question_not_ok_comment" => $v['step25_field1_fieldset']['step25_field1_question_not_ok_comment'],
			":data_relation" => "step25"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step7_data->id
		));
		$form_step25_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++)
		{
			if ($v['step25_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step25_data->id,
					":number" => $i + $form_step25_comment_data->max + 1,
					":comment" => $v['step25_field1_fieldset'][$i]["comment"],
					":data_relation" => "step25",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step25_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++
	} //$form_step25_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step25_feedback} (uid, question1, question_ok_not_ok, question_not_ok_comment, data_relation,inserted_on) VALUES (:uid,:question1, :question_ok_not_ok,:question_not_ok_comment, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step25_field1_fieldset']['step25_field1_question1'],
			":question_ok_not_ok" => $v['step25_field1_fieldset']['step25_field1_question_ok'],
			":question_not_ok_comment" => $v['step25_field1_fieldset']['step25_field1_question_not_ok_comment'],
			":data_relation" => "step25",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++)
		{
			if ($v['step25_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step25_field1_fieldset'][$i]["comment"],
					":data_relation" => "step25",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step25_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step25_field1_fieldset']["step25_comment_count"]; $i++
	}
	//$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success';
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step26/' . $user->uid;
}
/***************************************/
function step25_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step25_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step25_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step25_num_comment'] > 1)
	{
		$form_state['step25_num_comment']--;
	} //$form_state['step25_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step25_comment_add_more_callback($form, &$form_state)
{
	return $form['step25_field1_fieldset'];
}
/***************************************/
/***************************************** step 25 form ends ****************************/

/************************ Step 26 form starts *********************/
function ddcl_bb_splice_cover_plate_bolted_step26_form($form, &$form_state, $no_js_use = FALSE)
{
	global $base_url;
	global $user;
	drupal_set_title(t('Other recommendations'));
	// All the real form fields.
	$form = array();
	$form['step26_field1_fieldset'] = array(
		'#type' => 'fieldset',
		'#title' => '<strong>Any other recommendation/Comment?</strong>',
		'#tree' => TRUE,
		'#prefix' => '<div id="step26-field1-fieldset-wrapper">',
		'#suffix' => '</div>'
	);
	$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step26_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step26_feedback');
	$query->condition('uid', $user->uid);
	$form_step26_data = $query->execute();
	if ($form_step26_data)
	{
		if ($step26_data = $form_step26_data->fetchObject())
		{
			$form['step26_field1_fieldset']['step26_field1_question1'] = array(
				'#type' => 'hidden',
				'#default_value' => 'other recommendations/ Comments',
				'#required' => TRUE
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step26_data->id, $step26_data->data_relation);
			$icom = 1;
			$form['step26_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => ''
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step26_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step26_num_comment']))
			{
				$form_state['step26_num_comment'] = 1;
			} //empty($form_state['step26_num_comment'])
			$step26_temp1 = 0;
			for ($step26_i = 0; $step26_i < $form_state['step26_num_comment']; $step26_i++)
			{
				$step26_temp1 = $step26_i;
				$form['step26_field1_fieldset'][$step26_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step26_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step26_field1_fieldset']["step26_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step26_temp1
			);
			$form['step26_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step26_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step26_comment_add_more_callback',
					'wrapper' => 'step26-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step26_num_comment'] > 1)
			{
				$form['step26_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step26_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step26_comment_add_more_callback',
						'wrapper' => 'step26-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step26_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step26_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step26_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step26_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form['previous2'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step26_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Submit',
				'#attributes' => array(
					"onclick" => "return confirm('Are you sure?')"
				),
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step26_form_next_submit'
				)
			);
			$form['save_submit'] = array(
				'#type' => 'submit',
				'#value' => 'Save as draft',
				'#attributes' => array(
					"onclick" => "return confirm('Are you sure?')"
				),
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step26_form_save_submit'
				)
			);
		} //$step26_data = $form_step26_data->fetchObject()
		else
		{
			$form['step26_field1_fieldset']['step26_field1_question1'] = array(
				'#type' => 'hidden',
				'#default_value' => 'other recommendations/ Comments',
				'#required' => TRUE
			);
			$earlier_comments = _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step26_data->id, $step26_data->data_relation);
			$icom = 1;
			$form['step26_field1_fieldset']['existing_comments_title'] = array(
				'#markup' => ''
			);
			foreach ($earlier_comments as $rowcomment)
			{
				$form['step26_field1_fieldset']['existing_comments' . $icom] = array(
					'#markup' => $rowcomment
				);
				$icom++;
			} //$earlier_comments as $rowcomment
			if (empty($form_state['step26_num_comment']))
			{
				$form_state['step26_num_comment'] = 1;
			} //empty($form_state['step26_num_comment'])
			$step26_temp1 = 0;
			for ($step26_i = 0; $step26_i < $form_state['step26_num_comment']; $step26_i++)
			{
				$step26_temp1 = $step26_i;
				$form['step26_field1_fieldset'][$step26_i]["comment"] = array(
					"#type" => "textarea",
					"#title" => "Comment " . ($step26_temp1 + 1),
					"#default_value" => ""
				);
			} //$i = 0; $i < $form_state['step1_num_comment']; $i++
			$form['step26_field1_fieldset']["step26_comment_count"] = array(
				"#type" => "hidden",
				"#value" => $step26_temp1
			);
			$form['step26_field1_fieldset']['add_comment'] = array(
				'#type' => 'submit',
				'#value' => t('Add more comment'),
				'#limit_validation_errors' => array(),
				'#submit' => array(
					'step26_comment_add_more_add_one'
				),
				'#ajax' => array(
					'callback' => 'step26_comment_add_more_callback',
					'wrapper' => 'step26-field1-fieldset-wrapper'
				)
			);
			if ($form_state['step26_num_comment'] > 1)
			{
				$form['step26_field1_fieldset']['remove_comment'] = array(
					'#type' => 'submit',
					'#value' => t('Remove comment'),
					'#limit_validation_errors' => array(),
					'#submit' => array(
						'step26_comment_add_more_remove_one'
					),
					'#ajax' => array(
						'callback' => 'step26_comment_add_more_callback',
						'wrapper' => 'step26-field1-fieldset-wrapper'
					)
				);
			} //$form_state['step1_num_comment'] > 1
			if ($no_js_use)
			{
				if (!empty($form['step26_field1_fieldset']['remove_comment']['#ajax']))
				{
					unset($form['step26_field1_fieldset']['remove_comment']['#ajax']);
				} //!empty($form['step26_field1_fieldset']['remove_comment']['#ajax'])
				unset($form['step26_field1_fieldset']['add_comment']['#ajax']);
			} //$no_js_use
			$form['previous1'] = array(
				'#type' => 'submit',
				'#value' => 'Previous',
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step26_form_previous_submit'
				)
			);
			$form['next2'] = array(
				'#type' => 'submit',
				'#value' => 'Submit',
				'#attributes' => array(
					"onclick" => "return confirm('Are you sure?')"
				),
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step26_form_previous_submit'
				)
			);
			$form['save_submit'] = array(
				'#type' => 'submit',
				'#value' => 'Save as draft',
				'#attributes' => array(
					"onclick" => "return confirm('Are you sure?')"
				),
				'#submit' => array(
					'ddcl_bb_splice_cover_plate_bolted_step26_form_save_submit'
				)
			);
		} //$step26_data = $form_step26_data->fetchObject()
	} //$form_step26_data
	return $form;
}
function ddcl_bb_splice_cover_plate_bolted_step26_form_previous_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	/*$query = db_select('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->fields('ddcl_bb_splice_cover_plate_bolted_form_step8_feedback');
	$query->condition('uid', $user->uid);
	$form_step7_data = $query->execute()->fetchObject();
	*/
	$query = "SELECT * FROM ddcl_bb_splice_cover_plate_bolted_form_step26_feedback WHERE uid=:uid";
	$args = array(
		":uid" => $user->uid
	);
	$form_step26_data = db_query($query, $args);
	$form_step26_data_count = $form_step26_data->rowCount();
	$form_step26_data = $form_step26_data->fetchObject();	
	if ($form_step26_data_count != 0)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step26_feedback SET question1=:question1, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step26_field1_fieldset']['step26_field1_question1'],
			":data_relation" => "step26"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid ";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step26_data->id
		));
		$form_step26_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++)
		{
			if ($v['step26_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step26_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step26_form_id" => $form_step26_data->id,
					":number" => $i + $form_step26_comment_data->max + 1,
					":comment" => $v['step26_field1_fieldset'][$i]["comment"],
					":data_relation" => "step26",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step26_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++
	} //$form_step26_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step26_feedback} (uid, question1, data_relation,inserted_on) VALUES (:uid,:question1, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step26_field1_fieldset']['step26_field1_question1'],
			":data_relation" => "step26",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid ";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++)
		{
			if ($v['step26_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO 	ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step26_field1_fieldset'][$i]["comment"],
					":data_relation" => "step26",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step26_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/form/step25/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step26_form_next_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];	
	$query = "SELECT * FROM ddcl_bb_splice_cover_plate_bolted_form_step26_feedback WHERE uid=:uid";
	$args = array(
		":uid" => $user->uid
	);
	$form_step26_data = db_query($query, $args);
	$form_step26_data_count = $form_step26_data->rowCount();
	$form_step26_data = $form_step26_data->fetchObject();
	//var_dump($form_step26_data);die;
	if ($form_step26_data_count != 0)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step26_feedback SET question1=:question1, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step26_field1_fieldset']['step26_field1_question1'],
			":data_relation" => "step26"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid ";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 1
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step26_data->id
		));
		$form_step26_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++)
		{
			if ($v['step26_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $form_step26_data->id,
					":number" => $i + $form_step26_comment_data->max + 1,
					":comment" => $v['step26_field1_fieldset'][$i]["comment"],
					":data_relation" => "step26",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step26_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++
	} //$form_step26_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step26_feedback} (uid, question1, data_relation,inserted_on) VALUES (:uid,:question1, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step26_field1_fieldset']['step26_field1_question1'],
			":data_relation" => "step26",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid ";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++)
		{
			if ($v['step26_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO 	ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step26_field1_fieldset'][$i]["comment"],
					":data_relation" => "step26",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step8_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++
	}
	$form_state['redirect'] = 'ddcl-bb-splice-cover-plate-bolted/success/' . $user->uid;
}
function ddcl_bb_splice_cover_plate_bolted_step26_form_save_submit($form, &$form_state, $no_js_use = FALSE)
{
	global $user;
	$v = $form_state['values'];
	$v['step26_field1_fieldset']['step26_field1_question1'] = 'question 1';
	$query = "SELECT * FROM ddcl_bb_splice_cover_plate_bolted_form_step26_feedback WHERE uid=:uid";
	$args = array(
		":uid" => $user->uid
	);
	$form_step26_data = db_query($query, $args);
	$form_step26_data_count = $form_step26_data->rowCount();
	$form_step26_data = $form_step26_data->fetchObject();
	if ($form_step26_data_count != 0)
	{
		$query = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step26_feedback SET question1=:question1, data_relation=:data_relation WHERE uid=:uid ";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step26_field1_fieldset']['step26_field1_question1'],
			":data_relation" => "step26"
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$query = db_query(" SELECT MAX( number ) AS max FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id", array(
			':step1_form_id' => $form_step26_data->id
		));
		$form_step26_comment_data = $query->fetchObject();
		$comments = 0;
		for ($i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++)
		{
			if ($v['step26_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step26_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step26_form_id" => $form_step26_data->id,
					":number" => $i + $form_step26_comment_data->max + 1,
					":comment" => $v['step26_field1_fieldset'][$i]["comment"],
					":data_relation" => "step26",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step26_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++
	} //$form_step26_data
	else
	{
		$query = "INSERT INTO {ddcl_bb_splice_cover_plate_bolted_form_step26_feedback} (uid, question1, data_relation,inserted_on) VALUES (:uid,:question1, :data_relation,:inserted_on)";
		$args = array(
			":uid" => $user->uid,
			":question1" => $v['step26_field1_fieldset']['step26_field1_question1'],
			":data_relation" => "step26",
			":inserted_on" => date('Y-m-d')
		);
		/* storing the row id in $result */
		$result = db_query($query, $args, array(
			'return' => Database::RETURN_INSERT_ID
		));
		$queryfinish = "UPDATE ddcl_bb_splice_cover_plate_bolted_form_step1_feedback SET submitted=:submitted WHERE uid=:uid";
		$args_finish = array(
			":uid" => $user->uid,
			":submitted" => 0
		);
		/* storing the row id in $result */
		$resultfinish = db_query($queryfinish, $args_finish, array(
			'return' => Database::RETURN_INSERT_ID
		));
		/* For adding comments */
		$comments = 0;
		for ($i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++)
		{
			if ($v['step26_field1_fieldset'][$i]["comment"] != "")
			{
				$commentquery = "
	INSERT INTO ddcl_bb_splice_cover_plate_bolted_feedback_form_comment
	(step1_form_id, number, comment, data_relation, inserted_on)
	VALUES
	(:step1_form_id, :number, :comment, :data_relation, :inserted_on)
	";
				$commentargs = array(
					":step1_form_id" => $result,
					":number" => $i + 1,
					":comment" => $v['step26_field1_fieldset'][$i]["comment"],
					":data_relation" => "step26",
					":inserted_on" => date('Y-m-d')
				);
				/* storing the row id in $result */
				$commentresult = db_query($commentquery, $commentargs, array(
					'return' => Database::RETURN_INSERT_ID
				));
				if ($commentresult != 0)
				{
					$comments++;
				} //$commentresult != 0
			} //$v['step26_field1_fieldset'][$i]["comment"] != ""
		} //$i = 0; $i <= $v['step26_field1_fieldset']["step26_comment_count"]; $i++
	}
	drupal_set_message(t('You have successfully saved your feedback. You can anytime edit your feedback form.'), 'status');
	drupal_goto('home');
}
/***************************************/
function step26_comment_add_more_add_one($form, &$form_state)
{
	$form_state['step26_num_comment']++;
	$form_state['rebuild'] = TRUE;
	//$form_state['no_redirect'] = TRUE;
}
function step26_comment_add_more_remove_one($form, &$form_state)
{
	if ($form_state['step26_num_comment'] > 1)
	{
		$form_state['step26_num_comment']--;
	} //$form_state['step26_num_comment'] > 1
	$form_state['rebuild'] = TRUE;
}
function step26_comment_add_more_callback($form, &$form_state)
{
	return $form['step26_field1_fieldset'];
}
/***************************************/
/****************************************** step 26 form ends ****************************/
/**
 * Displays simple confirmation page after finishing the whole process.
 */
function ddcl_bb_splice_cover_plate_bolted_success()
{
	$data .= drupal_set_message(t('You have successfully submitted the feedback.'), 'status');
	$data .= drupal_goto('home');
	return $data;
}
/**********************************************/
function ddcl_bb_splice_cover_plate_bolted_result_page()
{
	/* get pending proposals to be approved */
	$output = "";
	$output .= l("Download All Result in CSV", "ddcl-bb-splice-cover-plate-bolted/form/result/download");
	$feedback_rows = array();
	$feedback_q = db_query('

select

step1.uid as "step1_uid",
step1.name as "step1_name",
step1.inserted_on as "step1_date",
step1.institute as "step1_institute",
step1.current_position as "step1_current_position",

step2.id as "step2_id",
step2.data_relation as "step2_data_relation",
step2.question1 as "step2_question1",
step2.question_ok_not_ok as "step2_question_ok_not_ok",
step2.question_not_ok_comment as "step2_question_not_ok_comment",


step3.id as "step3_id",
step3.data_relation as "step3_data_relation",
step3.question1 as "step3_question1",
step3.question_ok_not_ok as "step3_question_ok_not_ok",
step3.question_not_ok_comment as "step3_question_not_ok_comment",



step4.id as "step4_id",
step4.data_relation as "step4_data_relation",
step4.question1 as "step4_question1",
step4.question_ok_not_ok as "step4_question_ok_not_ok",
step4.question_not_ok_comment as "step4_question_not_ok_comment",


step5.id as "step5_id",
step5.data_relation as "step5_data_relation",
step5.question1 as "step5_question1",
step5.question_ok_not_ok as "step5_question_ok_not_ok",
step5.question_not_ok_comment as "step5_question_not_ok_comment",



step6.id as "step6_id",
step6.data_relation as "step6_data_relation",
step6.question1 as "step6_question1",
step6.question_ok_not_ok as "step6_question_ok_not_ok",
step6.question_not_ok_comment as "step6_question_not_ok_comment",


step7.id as "step7_id",
step7.data_relation as "step7_data_relation",
step7.question1 as "step7_question1",
step7.question_ok_not_ok as "step7_question_ok_not_ok",
step7.question_not_ok_comment as "step7_question_not_ok_comment",


step8.id as "step8_id",
step8.data_relation as "step8_data_relation",
step8.question1 as "step8_question1",
step8.question_ok_not_ok as "step8_question_ok_not_ok",
step8.question_not_ok_comment as "step8_question_not_ok_comment",


step9.id as "step9_id",
step9.data_relation as "step9_data_relation",
step9.question1 as "step9_question1",
step9.question_ok_not_ok as "step9_question_ok_not_ok",
step9.question_not_ok_comment as "step9_question_not_ok_comment",


step10.id as "step10_id",
step10.data_relation as "step10_data_relation",
step10.question1 as "step10_question1",
step10.question_ok_not_ok as "step10_question_ok_not_ok",
step10.question_not_ok_comment as "step10_question_not_ok_comment",


step11.id as "step11_id",
step11.data_relation as "step11_data_relation",
step11.question1 as "step11question1",
step11.question_ok_not_ok as "step11_question_ok_not_ok",
step11.question_not_ok_comment as "step11_question_not_ok_comment",

step12.id as "step12_id",
step12.data_relation as "step12_data_relation",
step12.question1 as "step12_question1",
step12.question_ok_not_ok as "step12_question_ok_not_ok",
step12.question_not_ok_comment as "step12_question_not_ok_comment",

step13.id as "step13_id",
step13.data_relation as "step13_data_relation",
step13.question1 as "step13_question1",
step13.question_ok_not_ok as "step13_question_ok_not_ok",
step13.question_not_ok_comment as "step13_question_not_ok_comment",

step14.id as "step14_id",
step14.data_relation as "step14_data_relation",
step14.question1 as "step14_question1",
step14.question_ok_not_ok as "step14_question_ok_not_ok",
step14.question_not_ok_comment as "step14_question_not_ok_comment",

step15.id as "step15_id",
step15.data_relation as "step15_data_relation",
step15.question1 as "step15_question1",
step15.question_ok_not_ok as "step15_question_ok_not_ok",
step15.question_not_ok_comment as "step15_question_not_ok_comment",

step16.id as "step16_id",
step16.data_relation as "step16_data_relation",
step16.question1 as "step16_question1",
step16.question_ok_not_ok as "step16_question_ok_not_ok",
step16.question_not_ok_comment as "step16_question_not_ok_comment",

step17.id as "step17_id",
step17.data_relation as "step17_data_relation",
step17.question1 as "step17_question1",
step17.question_ok_not_ok as "step17_question_ok_not_ok",
step17.question_not_ok_comment as "step17_question_not_ok_comment",

step18.id as "step18_id",
step18.data_relation as "step18_data_relation",
step18.question1 as "step18_question1",
step18.question_ok_not_ok as "step18_question_ok_not_ok",
step18.question_not_ok_comment as "step18_question_not_ok_comment",

step19.id as "step19_id",
step19.data_relation as "step19_data_relation",
step19.question1 as "step19_question1",
step19.question_ok_not_ok as "step19_question_ok_not_ok",
step19.question_not_ok_comment as "step19_question_not_ok_comment",

step20.id as "step20_id",
step20.data_relation as "step20_data_relation",
step20.question1 as "step20_question1",
step20.question_ok_not_ok as "step20_question_ok_not_ok",
step20.question_not_ok_comment as "step20_question_not_ok_comment",

step21.id as "step21_id",
step21.data_relation as "step21_data_relation",
step21.question1 as "step21_question1",
step21.question_ok_not_ok as "step21_question_ok_not_ok",
step21.question_not_ok_comment as "step21_question_not_ok_comment",

step22.id as "step22_id",
step22.data_relation as "step22_data_relation",
step22.question1 as "step22_question1",
step22.question_ok_not_ok as "step22_question_ok_not_ok",
step22.question_not_ok_comment as "step22_question_not_ok_comment",

step23.id as "step23_id",
step23.data_relation as "step23_data_relation",
step23.question1 as "step23_question1",
step23.question_ok_not_ok as "step23_question_ok_not_ok",
step23.question_not_ok_comment as "step23_question_not_ok_comment",

step24.id as "step24_id",
step24.data_relation as "step24_data_relation",
step24.question1 as "step24_question1",
step24.question_ok_not_ok as "step24_question_ok_not_ok",
step24.question_not_ok_comment as "step24_question_not_ok_comment",

step25.id as "step25_id",
step25.data_relation as "step25_data_relation",
step25.question1 as "step25_question1",
step25.question_ok_not_ok as "step25_question_ok_not_ok",
step25.question_not_ok_comment as "step25_question_not_ok_comment",

step26.id as "step26_id",
step26.data_relation as "step26_data_relation",
step26.question1 as "step26_question1"


from ddcl_bb_splice_cover_plate_bolted_form_step1_feedback step1

join ddcl_bb_splice_cover_plate_bolted_form_step2_feedback step2 on step1.uid=step2.uid
join ddcl_bb_splice_cover_plate_bolted_form_step3_feedback step3 on step2.uid=step3.uid
join ddcl_bb_splice_cover_plate_bolted_form_step4_feedback step4 on step3.uid=step4.uid
join ddcl_bb_splice_cover_plate_bolted_form_step5_feedback step5 on step4.uid=step5.uid
join ddcl_bb_splice_cover_plate_bolted_form_step6_feedback step6 on step5.uid=step6.uid
join ddcl_bb_splice_cover_plate_bolted_form_step7_feedback step7 on step6.uid=step7.uid
join ddcl_bb_splice_cover_plate_bolted_form_step8_feedback step8 on step7.uid=step8.uid
join ddcl_bb_splice_cover_plate_bolted_form_step9_feedback step9 on step8.uid=step9.uid
join ddcl_bb_splice_cover_plate_bolted_form_step10_feedback step10 on step9.uid=step10.uid
join ddcl_bb_splice_cover_plate_bolted_form_step11_feedback step11 on step10.uid=step11.uid
join ddcl_bb_splice_cover_plate_bolted_form_step12_feedback step12 on step11.uid=step12.uid
join ddcl_bb_splice_cover_plate_bolted_form_step13_feedback step13 on step12.uid=step13.uid
join ddcl_bb_splice_cover_plate_bolted_form_step14_feedback step14 on step13.uid=step14.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step15 on step14.uid=step15.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step16 on step15.uid=step16.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step17 on step16.uid=step17.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step18 on step17.uid=step18.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step19 on step18.uid=step19.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step20 on step19.uid=step20.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step21 on step20.uid=step21.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step22 on step21.uid=step22.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step23 on step22.uid=step23.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step24 on step23.uid=step24.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step25 on step24.uid=step25.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step26 on step25.uid=step26.uid

	');
	$i = 1;
	while ($feedback_data = $feedback_q->fetchObject())
	{
		$feedback_rows[$feedback_data->step1_uid] = array(
			$i,
			$feedback_data->step1_date,
			$feedback_data->step1_name,
			$feedback_data->step1_institute,
			$feedback_data->step1_current_position,
			$feedback_data->step2_question_ok_not_ok,
			$feedback_data->step2_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step2_id, $feedback_data->step2_data_relation),
			$feedback_data->step3_question_ok_not_ok,
			$feedback_data->step3_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step3_id, $feedback_data->step3_data_relation),
			$feedback_data->step4_question_ok_not_ok,
			$feedback_data->step4_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step4_id, $feedback_data->step4_data_relation),
			$feedback_data->step5_question_ok_not_ok,
			$feedback_data->step5_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step5_id, $feedback_data->step5_data_relation),
			$feedback_data->step6_question_ok_not_ok,
			$feedback_data->step6_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step6_id, $feedback_data->step6_data_relation),
			$feedback_data->step7_question_ok_not_ok,
			$feedback_data->step7_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step7_id, $feedback_data->step7_data_relation),
			$feedback_data->step8_question_ok_not_ok,
			$feedback_data->step8_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step8_id, $feedback_data->step8_data_relation),
			$feedback_data->step9_question_ok_not_ok,
			$feedback_data->step9_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step9_id, $feedback_data->step9_data_relation),
			$feedback_data->step10_question_ok_not_ok,
			$feedback_data->step10_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step10_id, $feedback_data->step10_data_relation),
			$feedback_data->step11_question_ok_not_ok,
			$feedback_data->step11_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step11_id, $feedback_data->step11_data_relation),
			$feedback_data->step12_question_ok_not_ok,
			$feedback_data->step12_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step12_id, $feedback_data->step12_data_relation),
			$feedback_data->step13_question_ok_not_ok,
			$feedback_data->step13_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step13_id, $feedback_data->step13_data_relation),
			$feedback_data->step14_question_ok_not_ok,
			$feedback_data->step14_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step14_id, $feedback_data->step14_data_relation),
			$feedback_data->step15_question_ok_not_ok,
			$feedback_data->step15_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step15_id, $feedback_data->step15_data_relation),
			$feedback_data->step16_question_ok_not_ok,
			$feedback_data->step16_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step16_id, $feedback_data->step16_data_relation),
			$feedback_data->step17_question_ok_not_ok,
			$feedback_data->step17_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step17_id, $feedback_data->step17_data_relation),
			$feedback_data->step18_question_ok_not_ok,
			$feedback_data->step18_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step18_id, $feedback_data->step18_data_relation),
			$feedback_data->step19_question_ok_not_ok,
			$feedback_data->step19_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step19_id, $feedback_data->step19_data_relation),
			$feedback_data->step20_question_ok_not_ok,
			$feedback_data->step20_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step20_id, $feedback_data->step20_data_relation),
			$feedback_data->step21_question_ok_not_ok,
			$feedback_data->step21_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step21_id, $feedback_data->step21_data_relation),
			$feedback_data->step22_question_ok_not_ok,
			$feedback_data->step22_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step22_id, $feedback_data->step22_data_relation),
			$feedback_data->step23_question_ok_not_ok,
			$feedback_data->step23_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step23_id, $feedback_data->step23_data_relation),
			$feedback_data->step24_question_ok_not_ok,
			$feedback_data->step24_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step24_id, $feedback_data->step24_data_relation),
			$feedback_data->step25_question_ok_not_ok,
			$feedback_data->step25_question_not_ok_comment,
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step25_id, $feedback_data->step25_data_relation),
			_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($feedback_data->step26_id, $feedback_data->step26_data_relation)
		);
		$i++;
	}
	//$pending_data = $pending_q->fetchObject()
	/* check if there are any pending proposals */
	if (!$feedback_q)
	{
		drupal_set_message(t('There are no results.'), 'status');
		return '';
	} //!$pending_rows
	$data_header = array(
		'No.',
		'Date of Submission',
		'Name',
		'Institute / Company',
		'Current Position',
		'Page 2 Material Strength',
		'Page 2 Material Strength not-ok comment',
		'Page 2 comments',
		'Page 3 Bolt-shear-black bolt',
		'Page 3 Bolt-shear-black bolt not-ok comment',
		'Page 3 comments',
		'Page 4 Bolt-shear-HSFG',
		'Page 4 Bolt-shear-HSFG not-ok comment',
		'Page 4 comments',
		'Page 5 Bolt-bearing-capacity',
		'Page 5 Bolt-bearing-capacity not-ok comment',
		'Page 5 comments',
		'Page 6 Bolt value ',
		'Page 6 Bolt value not-ok comment',
		'Page 6 comments',
		'Page 7 Bolt-numbers-and-group-capacity',
		'Page 7 Bolt-numbers-and-group-capacity not-ok comment',
		'Page 7 comments',
		'Page 8 Plate-height',
		'Page 8 Plate-height not-ok comment',
		'Page 8 comments',
		'Page 9 Plate-thickness',
		'Page 9 Plate-thickness not-ok comment',
		'Page 9 comments',
		'Page 10 Plate-block-shear',
		'Page 10 Plate-block-shear not-ok comment',
		'Page 10 comments',
		'Page 11 Weld-shear-strength',
		'Page 11 Weld-shear-strength not-ok comment',
		'Page 11 comments',
		'Page 12 Weld-minimum-thickness',
		'Page 12 Weld-minimum-thickness not-ok comment',
		'Page 12 comments',
		'Page 13 Detailing-checks-spacing',
		'Page 13 Detailing-checks-spacing not-ok comment',
		'Page 13 comments',
		'Page 14 Detailing-checks-end_edge',
		'Page 14 Detailing-checks-end_edge not-ok comment',
		'Page 14 comments',
		'Page 15 Sample',
		'Page 15 Sample',
		'Page 15 comments',
		'Page 16 Sample',
		'Page 16 Sample',
		'Page 16 comments',
		'Page 17 Sample',
		'Page 17 Sample',
		'Page 17 comments',
		'Page 18 Sample',
		'Page 18 Sample',
		'Page 18 comments',
		'Page 19 Sample',
		'Page 19 Sample',
		'Page 19 comments',
		'Page 20 Sample',
		'Page 20 Sample',
		'Page 20 comments',
		'Page 21 Sample',
		'Page 21 Sample',
		'Page 21 comments',
		'Page 22 Sample',
		'Page 22 Sample',
		'Page 22 comments',
		'Page 23 Sample',
		'Page 23 Sample',
		'Page 23 comments',
		'Page 24 Sample',
		'Page 24 Sample',
		'Page 24 comments',
		'Page 25 Sample',
		'Page 25 Sample',
		'Page 25 comments',
		'Page 26 Any other comments'
	);
	$output .= theme('table', array(
		'header' => $data_header,
		'rows' => $feedback_rows,
		'sticky' => FALSE
	));
	return $output;
}
//displayed in user page
function _fetch_existing_ddcl_bb_splice_cover_plate_bolted_comments($step_id, $data_relation)
{
	global $base_url;
	$query_for_comment = db_query("SELECT * FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id AND data_relation=:data_relation ORDER BY number ASC", array(
		':step1_form_id' => $step_id,
		':data_relation' => $data_relation
	));
	$comment = array();
	$i = 0;
	if ($query_for_comment != NULL)
	{
		while ($row = $query_for_comment->fetchObject())
		{
			$comment[$i] = $i + 1 . ") " . $row->comment . "<br><h6 style='text-align: right;'>
			<a href='{$base_url}/ddcl-bb-splice-cover-plate-bolted/delete/{$row->data_relation}/{$row->id}'>Delete</a><br>" . $row->inserted_on . "</h6><br>";
			$i++;
		} //$row = $query_for_comment->fetchObject()
	} //$query_for_comment == NULL
	else
	{
		$comment[$i] = 'No earlier comments';
	}
	return $comment;
}
function ddcl_bb_splice_cover_plate_bolted_delete_comment()
{
	global $base_url;
	$comment_id = arg(3);
	$comment_step = arg(2);
	if ($comment_id)
	{
		$query = "DELETE FROM {ddcl_bb_splice_cover_plate_bolted_feedback_form_comment} WHERE id = :id";
		$query_result = db_query($query, array(
			':id' => $comment_id
		));
		if ($query_result->rowCount() > 0)
		{
			drupal_set_message("Deleted");
		} //$query_result->rowCount() > 0
		else
		{
			drupal_set_message("MySQL Error: row deletion failed.");
		}
	} //$comment_id && user_access("osdag_feedback_form")
	drupal_goto("{$base_url}/ddcl-bb-splice-cover-plate-bolted/{$comment_step}/");
}
function _fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments($step_id, $data_relation)
{
	$query_for_comment = db_query("SELECT * FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id AND data_relation=:data_relation ORDER BY number ASC", array(
		':step1_form_id' => $step_id,
		':data_relation' => $data_relation
	));
	$comment = array();
	$i = 0;
	if ($query_for_comment != NULL)
	{
		while ($row = $query_for_comment->fetchObject())
		{
			$comment[$i] = $i + 1 . ") " . $row->comment . "<br><h6 style='text-align: right;'>" . $row->inserted_on . "</h6><br>";
			$i++;
		} //$row = $query_for_comment->fetchObject()
	} //$query_for_comment == NULL
	else
	{
		$comment[$i] = 'No earlier comments';
	}
	return $comment;
}
function _fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result($step_id, $data_relation)
{
	$query_for_comment = db_query("SELECT * FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id AND data_relation=:data_relation ORDER BY number ASC", array(
		':step1_form_id' => $step_id,
		':data_relation' => $data_relation
	));
	$text = "";
	$i = 0;
	while ($row = $query_for_comment->fetchObject())
	{
		if (strlen($row->comment) != 0)
		{
			$text .= $i + 1 . ") " . $row->comment . "<br>";
		} //strlen($row->comment) != 0
		else
		{
			$text .= 'No earlier comments';
		}
		$i++;
	} //$row = $query_for_comment->fetchObject()
	//$query_for_comment == NULL
	return $text;
}
function _fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($step_id, $data_relation)
{
	$query_for_comment = db_query("SELECT * FROM ddcl_bb_splice_cover_plate_bolted_feedback_form_comment WHERE step1_form_id = :step1_form_id AND data_relation=:data_relation ORDER BY number ASC", array(
		':step1_form_id' => $step_id,
		':data_relation' => $data_relation
	));
	$text = "";
	$i = 0;
	while ($row = $query_for_comment->fetchObject())
	{
		if (strlen($row->comment) != 0)
		{
			$text .= $i + 1 . ") " . $row->comment . "\n";
		} //strlen($row->comment) != 0
		else
		{
			$text .= 'No earlier comments';
		}
		$i++;
	} //$row = $query_for_comment->fetchObject()
	//$query_for_comment == NULL
	return trim($text);
}
function ddcl_bb_splice_cover_plate_bolted_result_generate_csv()
{
	global $user;
	if ($user->uid != NULL)
	{
		$result_dir = $_SERVER['DOCUMENT_ROOT'] . base_path() . "osdag-downloads/ddcl-bb-splice-cover-plate-bolted-result/{$user->uid}/";
		if (!file_exists($result_dir))
		{
			mkdir($result_dir, 0755, TRUE);
		} //!file_exists($result_dir)
		$result_file = $result_dir . "ddcl-bb-splice-cover-plate-bolted-result-{$user->uid}" . ".csv";
		$csv_file = "ddcl-bb-splice-cover-plate-bolted-result-{$user->uid}" . ".csv";
		$fp = fopen($result_file, "w");
		/* making the first row */
		$item = array(
			'No.',
		'Date of Submission',
		'Name',
		'Institute / Company',
		'Current Position',
		'Page 2 Material Strength',
		'Page 2 Material Strength not-ok comment',
		'Page 2 comments',
		'Page 3 Bolt-shear-black bolt',
		'Page 3 Bolt-shear-black bolt not-ok comment',
		'Page 3 comments',
		'Page 4 Bolt-shear-HSFG',
		'Page 4 Bolt-shear-HSFG not-ok comment',
		'Page 4 comments',
		'Page 5 Bolt-bearing-capacity',
		'Page 5 Bolt-bearing-capacity not-ok comment',
		'Page 5 comments',
		'Page 6 Bolt value ',
		'Page 6 Bolt value not-ok comment',
		'Page 6 comments',
		'Page 7 Bolt-numbers-and-group-capacity',
		'Page 7 Bolt-numbers-and-group-capacity not-ok comment',
		'Page 7 comments',
		'Page 8 Plate-height',
		'Page 8 Plate-height not-ok comment',
		'Page 8 comments',
		'Page 9 Plate-thickness',
		'Page 9 Plate-thickness not-ok comment',
		'Page 9 comments',
		'Page 10 Plate-block-shear',
		'Page 10 Plate-block-shear not-ok comment',
		'Page 10 comments',
		'Page 11 Weld-shear-strength',
		'Page 11 Weld-shear-strength not-ok comment',
		'Page 11 comments',
		'Page 12 Weld-minimum-thickness',
		'Page 12 Weld-minimum-thickness not-ok comment',
		'Page 12 comments',
		'Page 13 Detailing-checks-spacing',
		'Page 13 Detailing-checks-spacing not-ok comment',
		'Page 13 comments',
		'Page 14 Detailing-checks-end_edge',
		'Page 14 Detailing-checks-end_edge not-ok comment',
		'Page 14 comments',
		'Page 15 Sample',
		'Page 15 Sample',
		'Page 15 comments',
		'Page 16 Sample',
		'Page 16 Sample',
		'Page 16 comments',
		'Page 17 Sample',
		'Page 17 Sample',
		'Page 17 comments',
		'Page 18 Sample',
		'Page 18 Sample',
		'Page 18 comments',
		'Page 19 Sample',
		'Page 19 Sample',
		'Page 19 comments',
		'Page 20 Sample',
		'Page 20 Sample',
		'Page 20 comments',
		'Page 21 Sample',
		'Page 21 Sample',
		'Page 21 comments',
		'Page 22 Sample',
		'Page 22 Sample',
		'Page 22 comments',
		'Page 23 Sample',
		'Page 23 Sample',
		'Page 23 comments',
		'Page 24 Sample',
		'Page 24 Sample',
		'Page 24 comments',
		'Page 25 Sample',
		'Page 25 Sample',
		'Page 25 comments',
		'Page 26 Any other comments'
		);
		fputcsv($fp, $item);
		$query = 'select

step1.uid as "step1_uid",
step1.name as "step1_name",
step1.inserted_on as "step1_date",
step1.institute as "step1_institute",
step1.current_position as "step1_current_position",

step2.id as "step2_id",
step2.data_relation as "step2_data_relation",
step2.question1 as "step2_question1",
step2.question_ok_not_ok as "step2_question_ok_not_ok",
step2.question_not_ok_comment as "step2_question_not_ok_comment",


step3.id as "step3_id",
step3.data_relation as "step3_data_relation",
step3.question1 as "step3_question1",
step3.question_ok_not_ok as "step3_question_ok_not_ok",
step3.question_not_ok_comment as "step3_question_not_ok_comment",



step4.id as "step4_id",
step4.data_relation as "step4_data_relation",
step4.question1 as "step4_question1",
step4.question_ok_not_ok as "step4_question_ok_not_ok",
step4.question_not_ok_comment as "step4_question_not_ok_comment",


step5.id as "step5_id",
step5.data_relation as "step5_data_relation",
step5.question1 as "step5_question1",
step5.question_ok_not_ok as "step5_question_ok_not_ok",
step5.question_not_ok_comment as "step5_question_not_ok_comment",



step6.id as "step6_id",
step6.data_relation as "step6_data_relation",
step6.question1 as "step6_question1",
step6.question_ok_not_ok as "step6_question_ok_not_ok",
step6.question_not_ok_comment as "step6_question_not_ok_comment",


step7.id as "step7_id",
step7.data_relation as "step7_data_relation",
step7.question1 as "step7_question1",
step7.question_ok_not_ok as "step7_question_ok_not_ok",
step7.question_not_ok_comment as "step7_question_not_ok_comment",


step8.id as "step8_id",
step8.data_relation as "step8_data_relation",
step8.question1 as "step8_question1",
step8.question_ok_not_ok as "step8_question_ok_not_ok",
step8.question_not_ok_comment as "step8_question_not_ok_comment",


step9.id as "step9_id",
step9.data_relation as "step9_data_relation",
step9.question1 as "step9_question1",
step9.question_ok_not_ok as "step9_question_ok_not_ok",
step9.question_not_ok_comment as "step9_question_not_ok_comment",


step10.id as "step10_id",
step10.data_relation as "step10_data_relation",
step10.question1 as "step10_question1",
step10.question_ok_not_ok as "step10_question_ok_not_ok",
step10.question_not_ok_comment as "step10_question_not_ok_comment",


step11.id as "step11_id",
step11.data_relation as "step11_data_relation",
step11.question1 as "step11question1",
step11.question_ok_not_ok as "step11_question_ok_not_ok",
step11.question_not_ok_comment as "step11_question_not_ok_comment",

step12.id as "step12_id",
step12.data_relation as "step12_data_relation",
step12.question1 as "step12_question1",
step12.question_ok_not_ok as "step12_question_ok_not_ok",
step12.question_not_ok_comment as "step12_question_not_ok_comment",

step13.id as "step13_id",
step13.data_relation as "step13_data_relation",
step13.question1 as "step13_question1",
step13.question_ok_not_ok as "step13_question_ok_not_ok",
step13.question_not_ok_comment as "step13_question_not_ok_comment",

step14.id as "step14_id",
step14.data_relation as "step14_data_relation",
step14.question1 as "step14_question1",
step14.question_ok_not_ok as "step14_question_ok_not_ok",
step14.question_not_ok_comment as "step14_question_not_ok_comment",

step15.id as "step15_id",
step15.data_relation as "step15_data_relation",
step15.question1 as "step15_question1",
step15.question_ok_not_ok as "step15_question_ok_not_ok",
step15.question_not_ok_comment as "step15_question_not_ok_comment",

step16.id as "step16_id",
step16.data_relation as "step16_data_relation",
step16.question1 as "step16_question1",
step16.question_ok_not_ok as "step16_question_ok_not_ok",
step16.question_not_ok_comment as "step16_question_not_ok_comment",

step17.id as "step17_id",
step17.data_relation as "step17_data_relation",
step17.question1 as "step17_question1",
step17.question_ok_not_ok as "step17_question_ok_not_ok",
step17.question_not_ok_comment as "step17_question_not_ok_comment",

step18.id as "step18_id",
step18.data_relation as "step18_data_relation",
step18.question1 as "step18_question1",
step18.question_ok_not_ok as "step18_question_ok_not_ok",
step18.question_not_ok_comment as "step18_question_not_ok_comment",

step19.id as "step19_id",
step19.data_relation as "step19_data_relation",
step19.question1 as "step19_question1",
step19.question_ok_not_ok as "step19_question_ok_not_ok",
step19.question_not_ok_comment as "step19_question_not_ok_comment",

step20.id as "step20_id",
step20.data_relation as "step20_data_relation",
step20.question1 as "step20_question1",
step20.question_ok_not_ok as "step20_question_ok_not_ok",
step20.question_not_ok_comment as "step20_question_not_ok_comment",

step21.id as "step21_id",
step21.data_relation as "step21_data_relation",
step21.question1 as "step21_question1",
step21.question_ok_not_ok as "step21_question_ok_not_ok",
step21.question_not_ok_comment as "step21_question_not_ok_comment",

step22.id as "step22_id",
step22.data_relation as "step22_data_relation",
step22.question1 as "step22_question1",
step22.question_ok_not_ok as "step22_question_ok_not_ok",
step22.question_not_ok_comment as "step22_question_not_ok_comment",

step23.id as "step23_id",
step23.data_relation as "step23_data_relation",
step23.question1 as "step23_question1",
step23.question_ok_not_ok as "step23_question_ok_not_ok",
step23.question_not_ok_comment as "step23_question_not_ok_comment",

step24.id as "step24_id",
step24.data_relation as "step24_data_relation",
step24.question1 as "step24_question1",
step24.question_ok_not_ok as "step24_question_ok_not_ok",
step24.question_not_ok_comment as "step24_question_not_ok_comment",

step25.id as "step25_id",
step25.data_relation as "step25_data_relation",
step25.question1 as "step25_question1",
step25.question_ok_not_ok as "step25_question_ok_not_ok",
step25.question_not_ok_comment as "step25_question_not_ok_comment",

step26.id as "step26_id",
step26.data_relation as "step26_data_relation",
step26.question1 as "step26_question1"


from ddcl_bb_splice_cover_plate_bolted_form_step1_feedback step1

join ddcl_bb_splice_cover_plate_bolted_form_step2_feedback step2 on step1.uid=step2.uid
join ddcl_bb_splice_cover_plate_bolted_form_step3_feedback step3 on step2.uid=step3.uid
join ddcl_bb_splice_cover_plate_bolted_form_step4_feedback step4 on step3.uid=step4.uid
join ddcl_bb_splice_cover_plate_bolted_form_step5_feedback step5 on step4.uid=step5.uid
join ddcl_bb_splice_cover_plate_bolted_form_step6_feedback step6 on step5.uid=step6.uid
join ddcl_bb_splice_cover_plate_bolted_form_step7_feedback step7 on step6.uid=step7.uid
join ddcl_bb_splice_cover_plate_bolted_form_step8_feedback step8 on step7.uid=step8.uid
join ddcl_bb_splice_cover_plate_bolted_form_step9_feedback step9 on step8.uid=step9.uid
join ddcl_bb_splice_cover_plate_bolted_form_step10_feedback step10 on step9.uid=step10.uid
join ddcl_bb_splice_cover_plate_bolted_form_step11_feedback step11 on step10.uid=step11.uid
join ddcl_bb_splice_cover_plate_bolted_form_step12_feedback step12 on step11.uid=step12.uid
join ddcl_bb_splice_cover_plate_bolted_form_step13_feedback step13 on step12.uid=step13.uid
join ddcl_bb_splice_cover_plate_bolted_form_step14_feedback step14 on step13.uid=step14.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step15 on step14.uid=step15.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step16 on step15.uid=step16.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step17 on step16.uid=step17.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step18 on step17.uid=step18.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step19 on step18.uid=step19.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step20 on step19.uid=step20.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step21 on step20.uid=step21.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step22 on step21.uid=step22.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step23 on step22.uid=step23.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step24 on step23.uid=step24.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step25 on step24.uid=step25.uid
join ddcl_bb_splice_cover_plate_bolted_form_step15_feedback step26 on step25.uid=step26.uid

	';
	// $args = array(');
		$result = db_query($query);
		$i = 1;
		while ($feedback_data = $result->fetchObject())
		{
			$item = array(
				$i,
				$feedback_data->step1_date,
				$feedback_data->step1_name,
				$feedback_data->step1_institute,
				$feedback_data->step1_current_position,
				$feedback_data->step2_question_ok_not_ok,
				$feedback_data->step2_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step2_id, $feedback_data->step2_data_relation),
				$feedback_data->step3_question_ok_not_ok,
				$feedback_data->step3_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step3_id, $feedback_data->step3_data_relation),
				$feedback_data->step4_question_ok_not_ok,
				$feedback_data->step4_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step4_id, $feedback_data->step4_data_relation),
				$feedback_data->step5_question_ok_not_ok,
				$feedback_data->step5_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step5_id, $feedback_data->step5_data_relation),
				$feedback_data->step6_question_ok_not_ok,
				$feedback_data->step6_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step6_id, $feedback_data->step6_data_relation),
				$feedback_data->step7_question_ok_not_ok,
				$feedback_data->step7_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step7_id, $feedback_data->step7_data_relation),
				$feedback_data->step8_question_ok_not_ok,
				$feedback_data->step8_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step8_id, $feedback_data->step8_data_relation),
				$feedback_data->step9_question_ok_not_ok,
				$feedback_data->step9_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step9_id, $feedback_data->step9_data_relation),
				$feedback_data->step10_question_ok_not_ok,
				$feedback_data->step10_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step10_id, $feedback_data->step10_data_relation),
				$feedback_data->step11_question_ok_not_ok,
				$feedback_data->step11_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step11_id, $feedback_data->step11_data_relation),
				$feedback_data->step12_question_ok_not_ok,
				$feedback_data->step12_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step12_id, $feedback_data->step12_data_relation),
				$feedback_data->step13_question_ok_not_ok,
				$feedback_data->step13_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step13_id, $feedback_data->step13_data_relation),
				$feedback_data->step14_question_ok_not_ok,
				$feedback_data->step14_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step14_id, $feedback_data->step14_data_relation),
				$feedback_data->step15_question_ok_not_ok,
				$feedback_data->step15_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step15_id, $feedback_data->step15_data_relation),
				$feedback_data->step16_question_ok_not_ok,
				$feedback_data->step16_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step16_id, $feedback_data->step16_data_relation),
				$feedback_data->step17_question_ok_not_ok,
				$feedback_data->step17_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step17_id, $feedback_data->step17_data_relation),
				$feedback_data->step18_question_ok_not_ok,
				$feedback_data->step18_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step18_id, $feedback_data->step18_data_relation),
				$feedback_data->step19_question_ok_not_ok,
				$feedback_data->step19_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step19_id, $feedback_data->step19_data_relation),
				$feedback_data->step20_question_ok_not_ok,
				$feedback_data->step20_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step20_id, $feedback_data->step20_data_relation),
				$feedback_data->step21_question_ok_not_ok,
				$feedback_data->step21_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step21_id, $feedback_data->step21_data_relation),
				$feedback_data->step22_question_ok_not_ok,
				$feedback_data->step22_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step22_id, $feedback_data->step22_data_relation),
				$feedback_data->step23_question_ok_not_ok,
				$feedback_data->step23_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step23_id, $feedback_data->step23_data_relation),
				$feedback_data->step24_question_ok_not_ok,
				$feedback_data->step24_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step24_id, $feedback_data->step24_data_relation),
				$feedback_data->step25_question_ok_not_ok,
				$feedback_data->step25_question_not_ok_comment,
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step25_id, $feedback_data->step25_data_relation),
				_fetch_ddcl_bb_splice_cover_plate_bolted_existing_comments_result_csv($feedback_data->step26_id, $feedback_data->step26_data_relation)
			);
			fputcsv($fp, $item);
			$i++;
		} //$feedback_data = $result->fetchObject()
		fclose($fp);
		$file = $result_file;
		if (file_exists($file))
		{
			header('Content-Description: File Transfer');
			header('Content-Type: application/octet-stream');
			header('Content-Disposition: attachment; filename=' . basename($file));
			header('Expires: 0');
			header('Cache-Control: must-revalidate');
			header('Pragma: public');
			header('Content-Length: ' . filesize($file));
			ob_clean();
			flush();
			readfile($file);
			unlink($file);
			exit;
		} //file_exists($file)
	} //!$user->uid
	else
	{
		drupal_set_message(t('You do not have permission to access this page.'), 'error');
		drupal_goto('');
	}
}

