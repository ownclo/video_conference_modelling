#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <queue>

#define MAX_FRAME_SIZE 50000

int fact( int n )
{
	if(n == 0)
		return 1;

	return n * fact(n);
}

double binomCoef( int n, int k )
{
	//return (double)(fact(n)) / (fact(k) * fact(n - k));

	if (k > n) 
         return 0; 
     long long r = 1; 
     for (unsigned int d = 1; d <= k; ++d) 
     { 
         r *= n--; 
         r /= d; 
     } 
     return r; 
}

void calcStatData( int mas[], int mas_size, int shift, double &expected, double &variance, double &autocor )
{
	expected = variance = 0;

	for(int i = 0; i < mas_size; i++)
		expected += mas[i];
	expected /= mas_size;

	for(int i = 0; i < mas_size; i++)
		variance += (mas[i] - expected) * (mas[i] - expected);
	variance /= mas_size;

	double dif = 0;
	for(int i = 0; i < mas_size - shift; i++)
		dif += (mas[i] - expected) * (mas[i + shift] - expected);
	dif /= mas_size;

	autocor = dif / variance;
}

void calcStatData( double mas[], int mas_size, int shift, double &expected, double &variance, double &autocor )
{
	expected = variance = 0;

	for(int i = 0; i < mas_size; i++)
		expected += mas[i];
	expected /= mas_size;

	for(int i = 0; i < mas_size; i++)
		variance += (mas[i] - expected) * (mas[i] - expected);
	variance /= mas_size;

	double dif = 0;
	for(int i = 0; i < mas_size - shift; i++)
		dif += (mas[i] - expected) * (mas[i + shift] - expected);
	dif /= mas_size;

	autocor = dif / variance;
}

int max( int a, int b )
{
	return (a > b) ? a : b;
}

int min( int a, int b )
{
	return (a < b) ? a : b;
}

class NegBinDistr
{
public:
	double r;
	double p;

public:
	NegBinDistr( double expected, double variance )
	{
		p = expected / variance;
		r = expected * p / (1 - p);

		printf("Negative binomial distribution:\n\tp = %lf\n\tr = %lf\n", p, r);
	}

	int genVal()
	{
		int result = 0;
		for(int i = 0; i < r; i++)
		{
			double u_rand;
			while((u_rand = (double)rand() / RAND_MAX) == 0);
			int geom_rand = int(log(u_rand) / log(1 - p)) + 1;
			result += geom_rand;
		}

		return result;
	}
};

class DAR
{
private:
	double p, exp, var;
	int prev;
	NegBinDistr distr;

public:
	DAR( double autocor, double expected, double variance ) : distr(expected, variance), p(autocor), exp(expected), var(variance)
	{
		prev = distr.genVal();
	}

	int getNext()
	{
		if((double)rand() / RAND_MAX < p)
			return prev;
		else
			return prev = distr.genVal();
	}
};


class DAR2
{
private:
	//double p1, p2;
	double coef1, coef2;
	double exp, var;
	double prev, prev_prev;
	NegBinDistr distr;

public:
	//DAR2( double autocor_1, double autocor_2, double expected, double variance ) : distr(expected, variance), p1(autocor_1), p2(autocor_2), exp(expected), var(variance)
	DAR2( double a1, double a2, double expected, double variance ) : distr(expected, variance), coef1(a1), coef2(a2), exp(expected), var(variance)
	{
		prev = distr.genVal();
		prev_prev = distr.genVal();
	}

	double getNext()
	{
		////if((double)rand() / RAND_MAX < p)
		////	return prev;
		////else
		////	return prev = distr.genVal();

		//double new_val = coef1 * prev + coef2 * prev_prev + 0.12121212;
		////double new_val = coef1 * prev;

		double new_val;

		//if(prev == prev_prev)
		//{
		//	if((double)rand() / RAND_MAX < 0.867)
		//		new_val = prev;
		//	else
		//		new_val = distr.genVal();
		//}
		//else
		//{
		//	if((double)rand() / RAND_MAX < 0.674)
		//		new_val = prev;
		//	else
		//		new_val = prev_prev;
		//}


		double p_aba, p_abb, p_abc, p_aaa;

		// For correlation calculated by Excel
		//p_aaa = 0.867;
		//p_abb = 0.674;
		//p_abc = 0;

		//p_aaa = 0.8965;
		//p_abb = 0.5236;
		//p_abc = 0.3;

		//p_aaa = 0.9163;
		//p_abb = 0.4236;
		//p_abc = 0.5;

		
		// For correlation calculated by calcStatDat() function of this program
		//p_aaa = 0.89058;
		//p_abb = 0.52674;
		//p_abc = 0.3;

		// p1 = 0.6, p2 = 0.3
		p_aaa = (double)9 / 14;  //x3
		p_abb = (double)5 / 6;   //x1
		p_abc = 0.3;


		p_aba = 1 - p_abb - p_abc;

		if(prev == prev_prev)
		{
			if((double)rand() / RAND_MAX < p_aaa)
				new_val = prev;
			else
				new_val = distr.genVal();
		}
		else
		{
			double rand_num = (double)rand() / RAND_MAX;

			if(rand_num < p_abc)
				new_val = distr.genVal();
			else
			{
				if(rand_num < p_abc + p_abb)
					new_val = prev;
				else
					new_val = prev_prev;
			}
		}

	
		//new_val = coef1 * prev + coef2 * prev_prev + distr.genVal();

		//double p = 0.5;
		//if((double)rand() / RAND_MAX < p)
		//{
		//	new_val = distr.genVal();
		//}
		//else
		//{
		//	//if((double)rand() / RAND_MAX < coef1 * )
		//}

		prev_prev = prev;
		prev = new_val;

		return new_val;
	}
};



class DecoderBufferModel
{
private:
	DAR dar;
	int chan_capacity;
	int coder_buf_cur_size;
	int decoder_buf_cur_size;
	std::queue<int> frames_queue;

public:
	DecoderBufferModel( DAR dar_model, int init_delay, int channel_capacity ) : dar(dar_model), chan_capacity(channel_capacity)
	{
		//printf("\n\nPREBUFFERING\n");
		coder_buf_cur_size = decoder_buf_cur_size = 0;
		for(int i = 0; i < init_delay; i++)
		{
			int new_frame = dar.getNext();
			int data_to_send = min(coder_buf_cur_size, chan_capacity);

			frames_queue.push(new_frame);
			coder_buf_cur_size += new_frame;
			coder_buf_cur_size -= data_to_send;

			decoder_buf_cur_size += data_to_send;
			//printf("New frame: %5d;  Sending: %5d;     (coder: %6d  |  decoder: %6d)\n", new_frame, data_to_send, coder_buf_cur_size, decoder_buf_cur_size);
		}
		printf("\n");
	}

	bool startModeling( int max_frames_num, int &processed_frames_num, int &final_buf_size )
	{
		//printf("MODELLING\n");
		int i = 0;
		while(i < max_frames_num)
		{
			int new_frame = dar.getNext();
			int data_to_send = min(coder_buf_cur_size, chan_capacity);

			frames_queue.push(new_frame);
			coder_buf_cur_size += new_frame;
			coder_buf_cur_size -= data_to_send;

			decoder_buf_cur_size += data_to_send;
			decoder_buf_cur_size -= frames_queue.back();
			frames_queue.pop();
			//printf("New frame: %5d;  Sending: %5d;     (coder: %6d  |  decoder: %6d)\n", new_frame, data_to_send, coder_buf_cur_size, decoder_buf_cur_size);

			if(decoder_buf_cur_size < 0)
				break;

			i++;
		}

		processed_frames_num = i;
		final_buf_size = decoder_buf_cur_size;
		return (decoder_buf_cur_size >= 0);
	}
};

class EvseevModeling
{
private:
	const int chan_capacity;
	const int playback_delay;
	DAR dar;

public:
	EvseevModeling( DAR dar, int playback_delay, int channel_capacity ) :
	  dar (dar), chan_capacity (channel_capacity), playback_delay (playback_delay) {}

	bool startModeling( int max_frames_num, int &frame_num )
	{
		double t = 0;
		for(frame_num = 0; frame_num < max_frames_num; frame_num++)
		{
			t = ((t <= frame_num) ? frame_num : t) + (double)dar.getNext() / chan_capacity;
			if(t > frame_num + playback_delay)
				return false;
		}
		return true;
	}
};

int main(int argc, const char *argv[])
{
	srand(time(NULL));
	double expected, variance, autocor;
	//const int N = 49;
	//int mas[N] = {4554, 4471, 4201, 4652, 4597, 3751, 4602, 4393, 4724, 4584, 4353, 4949, 5198, 4703, 5175, 4899, 4412, 4256, 4024, 3633, 3237, 3831, 3771, 3901, 3882, 3755, 2324, 3204, 2397, 3503, 3576, 4289, 4058, 3667, 3945, 4135, 4404, 4124, 4019, 3403, 3811, 3697, 3928, 3981, 3808, 3413, 4436, 4716, 4590};

	FILE *frames_file = fopen("frames_QP5.txt", "r");
	if(frames_file == NULL)
	{
		printf("Can't open the file\n");
		return -1;
	}
	int N = 0;
	int tmp;
	while(fscanf(frames_file, "%i", &tmp) != EOF)
		N++;
	printf("N = %i\n", N);

	fseek(frames_file, 0, SEEK_SET);
	
	int *mas = new int[N];
	for(int i = 0; i < N; i++)
		fscanf(frames_file, "%i", &mas[i]);

	double autocor2;
	calcStatData(mas, N, 2, expected, variance, autocor2);
	calcStatData(mas, N, 1, expected, variance, autocor);
	printf("Expected value:   %lf\nVariance:         %lf\nAutocorrilation (shift = 1):   %lf\nAutocorrilation (shift = 2):   %lf\n\n", expected, variance, autocor, autocor2);


	//DAR2 dar2(0.10936, -0.8689746, expected, variance);
	DAR2 dar2(0.6116, 0.2672, expected, variance);

	const int DAR2_TRIALS_NUM = 100000;
	double *mas_dar2 = new double[DAR2_TRIALS_NUM];
	for(int i = 0; i < DAR2_TRIALS_NUM; i++)
	{
		mas_dar2[i] = dar2.getNext();
		//printf("%i: %.1lf\n", i, mas_dar2[i]);
	}
	
	double cor_1, cor_2;
	calcStatData(mas_dar2, DAR2_TRIALS_NUM, 1, expected, variance, cor_1);
	calcStatData(mas_dar2, DAR2_TRIALS_NUM, 2, expected, variance, cor_2);
	printf("\nExpected value:   %lf\nVariance:         %lf\nAutocorrilation (shift = 1):   %lf\nAutocorrilation (shift = 2):   %lf\n\n", expected, variance, cor_1, cor_2);

	delete [] mas_dar2;
	exit(1);


#ifndef MODEL_CHECK
	{
		DAR dar(autocor, expected, variance);
		FILE *model_file = fopen("Modeling_frames.csv", "w");
		for(int i = 0; i < N; i++)
			fprintf(model_file, "%i\n", dar.getNext());
		fclose(model_file);
	}

	double orig_hist[MAX_FRAME_SIZE] = {0};
	for(int i = 0; i < N; i++)
		orig_hist[mas[i]]++;

	int trails_num = 1;
	int frames_num = N;
	double avg_hist[MAX_FRAME_SIZE] = {0};
	printf("\n");
	for(int i = 0; i < trails_num; i++)
	{
		printf("Modeling. Trial %i/%i\r", i + 1, trails_num);
		DAR dar(autocor, expected, variance);
		for(int j = 0; j < frames_num; j++)
			avg_hist[dar.getNext()]++;
	}
	printf("\n");

	for(int i = 0; i < MAX_FRAME_SIZE; i++)
		avg_hist[i] /= trails_num;

	int max_not_null_i = 0;
	int min_not_null_i = 0;
	for(int i = 0; i < MAX_FRAME_SIZE; i++)
		if(avg_hist[i] != 0  ||  orig_hist[i] != 0)
			max_not_null_i = i;
	while(avg_hist[min_not_null_i] == 0  &&  orig_hist[min_not_null_i] == 0)
		min_not_null_i++;

	FILE *hist_f = fopen("hist.csv", "w");
	fprintf(hist_f, "x;Orig. hist.;Modeling hist\n");
	for(int i = min_not_null_i; i <= max_not_null_i; i++)
		fprintf(hist_f, "%i;%.5lf;%.5lf\n", i, orig_hist[i], avg_hist[i]);
	fclose(hist_f);

#endif


	//double expected2, variance2, autocor2;
	//NegBinDistr test_distr(expected, variance);
	//int sum = 0;
	//const int N2 = 100000;
	//int mas2[N2];
	//for(int i = 0; i < N2; i++)
	//	mas2[i] = test_distr.genVal();
	//calcStatData(mas2, N2, 1, expected2, variance2, autocor2);
	//printf("\n\nExpected value:   %lf\nVariance:         %lf\nAutocorrilation:  %lf\n\n", expected2, variance2, autocor2);

	//test_distr.p /= 10;
	//for(int i = 0; i < N2; i++)
	//	mas2[i] = test_distr.genVal();
	//calcStatData(mas2, N2, 1, expected2, variance2, autocor2);
	//printf("Expected value:   %lf\nVariance:         %lf\nAutocorrilation:  %lf\n\n", expected2, variance2, autocor2);
	//exit(1);


#ifdef MODELING
	srand(time(NULL));
	FILE *output = fopen("Capacity_success_prob.csv", "w");
	fprintf(output, "Capacity;Successful trials rate\n");
	int n_trials = 5000;
	for(double chan_capacity = expected + 0.09 * expected; chan_capacity < expected + 0.3 * expected; chan_capacity += 0.003 * expected)
	{
		int successful_trials_num = 0;
		for(int i = 0; i < n_trials; i++)
		{
			int rand_seed = time(NULL);
			int init_delay = 15;
			int max_frames_num = 5000;
			int processed_frames_num;

													//printf("\nChannel capacity: %.3lf\n", ((double)i / n_trials - 0.27) * 0.3);
		//fprintf(output, "%.3lf;", ((double)i / n_trials - 0.27) * 0.3);
		////srand(rand_seed);
		//DAR dar(autocor, expected, variance);
		//DecoderBufferModel model(dar, init_delay, chan_capacity);
		//model.startModeling(max_frames_num, processed_frames_num, final_buf_size);
		////printf("\n\n------------------------------\nModel1:\n------------------------------\nModeling complete\nFrame processed: %i / %i\nFinal buffer size: %i\n\n\n", processed_frames_num, max_frames_num, final_buf_size);
		//printf("Model1: Frame processed: %5d / %i\n", processed_frames_num, max_frames_num);
		//fprintf(output, "%i;", processed_frames_num);

		//srand(rand_seed);
			DAR dar2(autocor, expected, variance);
			EvseevModeling model2(dar2, init_delay, chan_capacity);
			model2.startModeling(max_frames_num, processed_frames_num);
			//printf("\n\n------------------------------\nModel2:\n------------------------------\nModeling complete\nFrame processed: %i / %i\n", processed_frames_num, max_frames_num);
			//printf("Evseev model: Frame processed: %5d / %i\n", processed_frames_num, max_frames_num);
			//fprintf(output, "%i\n", processed_frames_num);

			successful_trials_num += (processed_frames_num == max_frames_num) ? 1 : 0;
		}
		printf("Capacity = %lf;   Success rate = %lf\n", chan_capacity, (double)successful_trials_num / n_trials);
		fprintf(output, "%lf;%lf\n", chan_capacity, (double)successful_trials_num / n_trials);
	}
	fclose(output);
#endif

    return 0;
}
