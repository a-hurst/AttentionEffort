# -*- coding: utf-8 -*-

__author__ = "Austin Hurst"

import klibs
from klibs import P
from klibs.KLExceptions import TrialException
from klibs.KLUtilities import deg_to_px, pump, flush, show_mouse_cursor, hide_mouse_cursor
from klibs.KLGraphics import fill, flip, blit
from klibs.KLUserInterface import any_key, key_pressed, ui_request
from klibs.KLGraphics import KLDraw as kld
from klibs.KLCommunication import message
from klibs.KLResponseCollectors import KeyPressResponse, Response
from klibs.KLTime import CountDown

import random
import time
import sdl2

from InterfaceExtras import ThoughtProbe, LikertType, Slider, Button

WHITE = (255, 255, 255, 255)
MID_RED = (255, 128, 128, 255)
MID_GREEN =  (128, 255, 128, 255)
TRANSPARENT_GREY = (192, 192, 192, 64)
TRANSLUCENT_WHITE = (192, 192, 192, 128)


class AttentionEffort(klibs.Experiment):

    def setup(self):

        # Initialize stimulus sizes

        mask_size_x = deg_to_px(3.0)
        mask_size_ring = deg_to_px(4.0)
        mask_thick = deg_to_px(0.3)

        # Initialize text styles
        self.txtm.add_style('normal', '0.7deg')
        self.txtm.add_style('title', '1.0deg')

        self.mask_x = kld.Asterisk(mask_size_x, mask_thick, fill=P.default_color, spokes=8)
        self.mask_ring = kld.Annulus(mask_size_ring, mask_thick, fill=P.default_color)

        self.digits = {}
        digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for digit in digits:
            self.digits[digit] = {}
        
        self.sizes = ['1.5deg', '2.0deg', '2.5deg', '3.0deg', '3.5deg']
        for size in self.sizes:
            self.txtm.add_style(size, size)

        for digit in digits:
            for size in self.sizes:
                self.digits[digit][size] = message(str(digit), style = size, blit_txt = False)

        # Initialize thought probes

        p_title = message(P.probe_question, "title", blit_txt=False)
        p_responses = P.probe_responses
        p_order = P.probe_order
        p_origin = (P.screen_c[0], P.screen_x//10)
        self.probe = ThoughtProbe(p_responses, p_title, int(P.screen_x*0.8), p_origin, p_order)

        # Initialize effort probes

        qeffort_text = "How much effort were you putting into staying on-task?"
        self.effort_q = message(qeffort_text, "title", blit_txt=False)
        self.mineffort_msg = message("0%", "normal", blit_txt=False)
        self.maxeffort_msg = message("100%", "normal", blit_txt=False)
        self.submit_msg = message("Continue", "normal", blit_txt=False)
        pad = int(self.submit_msg.height * 0.75)
        self.submit = Button(
            self.submit_msg, int(self.submit_msg.width + pad * 1.5), self.submit_msg.height + pad,
            registration=8, location=(P.screen_c[0], int(P.screen_y * 0.8))
        )

        # Randomly distribute probes across session, avoiding placing them less than 20 sec. apart

        self.probe_trials = []
        noprobe_span = [False] * P.noprobe_span
        probe_span = [True] + [False] * (P.probe_span - 1)
        while len(self.probe_trials) < (P.trials_per_block * P.blocks_per_experiment):
            random.shuffle(probe_span)
            self.probe_trials += noprobe_span + probe_span

        # Show task instructions and example thought probe

        self.instructions()

        # Add practice blocks to start of task

        self.first_nonpractice = 1
        if P.run_practice_blocks:
            num_nonpractice = P.blocks_per_experiment
            self.insert_practice_block(1, trial_counts=9, factor_mask={'number': range(1, 10)})
            self.insert_practice_block(2, trial_counts=9, factor_mask={'number': range(1, 10)})
            self.first_nonpractice = P.blocks_per_experiment - num_nonpractice + 1


    def instructions(self):

        p1 = ("During this task, you will presented with a sequence of numbers in the middle of "
            "the screen.\n\nPress any key to see an example.")
        p2 = ("Your task will be to press the [space] key as quickly as possible whenever a "
            "number other than {0} appears, and to withhold your response whenever the number "
            "is {0}.\n\nPress any key to continue.".format(P.target))
        p3 = ("Occasionally, the task will be interrupted by screens asking you about your "
            "focus just prior.\nWhen this happens, please select the most accurate "
            "response using the mouse cursor.\n\nPress any key to see an example.")
        p4 = ("After responding, you will be asked how much effort you "
            "were putting into staying focused on the task before the interruption.\n\n"
            "When this happens, please answer using the scale from 0% to 100% that will appear "
            "on screen. Your responses will be anonymous so please answer honestly.\n\n"
            "Press any key to see an example.")

        msg1 = message(p1, 'normal', blit_txt=False, align='center')
        msg2 = message(p2, 'normal', blit_txt=False, align='center', wrap_width=int(P.screen_x*0.8))
        msg3 = message(p3, 'normal', blit_txt=False, align='center', wrap_width=int(P.screen_x*0.8))
        msg4 = message(p4, 'normal', blit_txt=False, align='center', wrap_width=int(P.screen_x*0.8))

        # First page of instructions

        flush()
        fill()
        blit(msg1, 5, P.screen_c)
        flip()
        any_key(allow_mouse_click=False)

        # Example stimuli

        numlist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(numlist)
        for n in numlist[1:5]:
            trialtime = CountDown(1.125)
            numsize = random.choice(self.sizes)
            while trialtime.counting():
                ui_request()
                fill()
                mask_on = trialtime.elapsed() > 0.25
                if mask_on:
                    blit(self.mask_x, 5, P.screen_c)
                    blit(self.mask_ring, 5, P.screen_c)
                else:
                    blit(self.digits[n][numsize], 5, P.screen_c)
                flip()
        
        # Task explanation/illustration

        flush()
        fill()
        blit(msg2, 5, P.screen_c)
        flip()
        any_key(allow_mouse_click=False)

        # Probe explanation + example probe

        fill()
        blit(msg3, 5, P.screen_c)
        flip()
        any_key(allow_mouse_click=False)
        self.probe.collect()

        # Slider explanation + example slider

        fill()
        blit(msg4, 5, P.screen_c)
        flip()
        any_key(allow_mouse_click=False)
        self.get_effort()


    def block(self):

        # Generate font sizes to use for numbers during the block

        self.num_sizes = []
        while len(self.num_sizes) <= P.trials_per_block:
            self.num_sizes = self.num_sizes + self.sizes
        random.shuffle(self.num_sizes)
        self.num_sizes = self.num_sizes[0:P.trials_per_block]

        # Generate block message

        header = ""#"Block {0} of {1}".format(P.block_number, P.blocks_per_experiment)
        instructions = (
            "Please press the space key quickly when a digit other than {0} \nappears on screen, "
            "and withhold your response when the digit is {0}.".format(P.target)
        )
        if P.practicing:
            header = "This is a practice block."
            instructions = instructions + "\nYou will be given feedback on your accuracy."
        msg = message(header+"\n\n"+instructions, 'normal', align="center", blit_txt=False)
        start_msg = message("Press the [space] key to start.", 'normal', blit_txt=False)

        # Show block message, and wait for input before staring block

        if P.block_number in [1, self.first_nonpractice]:
            message_interval = CountDown(2)
            while message_interval.counting():
                ui_request() # Allow quitting during loop
                fill()
                blit(msg, 8, (P.screen_c[0], int(P.screen_y*0.15)))
                flip()

            while True:
                if key_pressed(' '):
                    break
                fill()
                blit(msg, 8, (P.screen_c[0], int(P.screen_y*0.15)))
                blit(start_msg, 5, (P.screen_c[0], int(P.screen_y*0.75)))
                flip()
            
    
    def setup_response_collector(self):

        # Configure ResponseCollector for collecting responses via keyboard

        self.rc.uses([KeyPressResponse])
        self.rc.display_callback = self.sart_callback
        self.rc.end_collection_event = 'trial_end'
        self.rc.keypress_listener.interrupts = True
        self.rc.keypress_listener.key_map = {' ': 'go'}


    def trial_prep(self):

        # Set trial flags

        self.mask_on = False
        self.num_size = self.num_sizes.pop()
        self.probe_trial = False if P.practicing else self.probe_trials.pop(0)

        # Specifiy sequence/onsets of events for the trial

        self.evm.register_ticket(['mask_on', P.stim_duration])
        self.evm.register_ticket(['trial_end', P.trial_duration])


    def trial(self):

        fill()
        blit(self.digits[self.number][self.num_size], 5, P.screen_c)
        flip()
        
        self.rc.collect()
        response = self.rc.keypress_listener.response()
        
        if response.rt == klibs.TIMEOUT:
            resp, rt = ['nogo', 'NA']
        else:
            resp, rt = response
        correct_resp = 'nogo' if self.number == P.target else 'go'
        accuracy = resp == correct_resp

        while self.evm.before('trial_end'):
            ui_request()
            fill()
            blit(self.mask_x, 5, P.screen_c)
            blit(self.mask_ring, 5, P.screen_c)
            flip()

        if P.practicing:
            if accuracy == False:
                feedback = "Incorrect! "
                if correct_resp == 'nogo':
                    feedback += "Please withhold responses to the digit {0}.".format(P.target)
                else:
                    feedback += "Please respond quickly to digits other than {0}.".format(P.target)
            else:
                feedback = "Correct response!"
            feedback_msg = message(feedback, 'normal', blit_txt=False)
            feedback_timer = CountDown(1.5)
            while feedback_timer.counting():
                ui_request()
                fill()
                blit(feedback_msg, 5, P.screen_c)
                flip()

        # If probe trial, present MW probe and wait for response + keypress before ending trial

        if self.probe_trial:
            probe_resp, probe_rt = self.probe.collect()
            eff_level, eff_rt = self.get_effort()
            probe_rt = probe_rt * 1000 # convert seconds to ms
            eff_rt = eff_rt * 1000 # convert seconds to ms
            eff_level = eff_level * 100 # scale range to 0% - 100%
            resume_msg = message("Press the [space] key to resume the task.", 'title', blit_txt=False)
            while True:
                if key_pressed(' '):
                    break
                fill()
                blit(resume_msg, 5, P.screen_c)
                flip()
        else:
            probe_resp, probe_rt, eff_level, eff_rt = ('NA', 'NA', 'NA', 'NA')

        return {
            "practicing": P.practicing,
            "block_num": P.block_number,
            "trial_num": P.trial_number,
            "digit": self.number,
            "digit_size": self.num_size,
            "target_digit": P.target,
            "response": resp,
            "rt": rt,
            "accuracy": accuracy,
            "probe_resp": probe_resp,
            "probe_rt": probe_rt,
            "effort_level": eff_level,
            "effort_rt": eff_rt
        }


    def trial_clean_up(self):
        pass


    def clean_up(self):
        pass


    def sart_callback(self):

        if self.evm.after('mask_on') and not self.mask_on:
            fill()
            blit(self.mask_x, 5, P.screen_c)
            blit(self.mask_ring, 5, P.screen_c)
            flip()
            self.mask_on = True


    def get_effort(self):

        slider_loc = (P.screen_c[0], int(P.screen_y*0.55))
        slider_cols = {'line': WHITE, 'slider': TRANSLUCENT_WHITE}
        scale = Slider(int(P.screen_x*0.75), ticks=5, location=slider_loc, fills=slider_cols)
        label_pad = scale.tick.surface_height
        
        show_mouse_cursor()
        onset = time.time()
        while True:
            sq = pump(True)
            ui_request(queue=sq)
            fill()
            blit(self.effort_q, 5, (P.screen_c[0], int(P.screen_y*0.3)))
            blit(self.mineffort_msg, 8, (scale.xmin, slider_loc[1] + label_pad))
            blit(self.maxeffort_msg, 8, (scale.xmax, slider_loc[1] + label_pad))
            scale.draw()
            if scale.pos != None:
                self.submit.draw()
            flip()
            scale.listen(sq)
            if scale.pos != None:
                if self.submit.listen(sq) or key_pressed('Return', queue=sq):
                    rt = time.time() - onset
                    hide_mouse_cursor()
                    return (scale.pos, rt)



class LikertProbe(object):

    def __init__(self, first, last, question, width, origin):

        self.q = question
        self.width = width
        self.origin = origin

        height = width / (len(range(first, last+1)) + 2)
        self.scale = LikertType(first, last, width, height, style='normal')

    def collect(self):

        show_mouse_cursor()
        onset = time.time()

        while self.scale.response == None:
            q = pump(True)
            ui_request(queue=q)
            fill()
            blit(self.q, location=self.origin, registration=8)
            self.scale.response_listener(q)
            flip()

        response = self.scale.response
        rt = time.time() - onset
        hide_mouse_cursor()
        self.scale.response = None # reset for next time
        return Response(response, rt)
