#include "objects.h"
#include "code_objects/synapses_pre_codeobject.h"
#include "brianlib/common_math.h"
#include "brianlib/stdint_compat.h"
#include<cmath>
#include<ctime>
#include<iostream>
#include<fstream>
#include<climits>
#include "brianlib/stdint_compat.h"
#include "synapses_classes.h"

////// SUPPORT CODE ///////
namespace {
 	
 template <typename T>
 static inline T _clip(const T value, const double a_min, const double a_max)
 {
     if (value < a_min)
         return a_min;
     if (value > a_max)
         return a_max;
     return value;
 }
 template < typename T1, typename T2 > struct _higher_type;
 template < > struct _higher_type<int,int> { typedef int type; };
 template < > struct _higher_type<int,long> { typedef long type; };
 template < > struct _higher_type<int,long long> { typedef long long type; };
 template < > struct _higher_type<int,float> { typedef float type; };
 template < > struct _higher_type<int,double> { typedef double type; };
 template < > struct _higher_type<int,long double> { typedef long double type; };
 template < > struct _higher_type<long,int> { typedef long type; };
 template < > struct _higher_type<long,long> { typedef long type; };
 template < > struct _higher_type<long,long long> { typedef long long type; };
 template < > struct _higher_type<long,float> { typedef float type; };
 template < > struct _higher_type<long,double> { typedef double type; };
 template < > struct _higher_type<long,long double> { typedef long double type; };
 template < > struct _higher_type<long long,int> { typedef long long type; };
 template < > struct _higher_type<long long,long> { typedef long long type; };
 template < > struct _higher_type<long long,long long> { typedef long long type; };
 template < > struct _higher_type<long long,float> { typedef float type; };
 template < > struct _higher_type<long long,double> { typedef double type; };
 template < > struct _higher_type<long long,long double> { typedef long double type; };
 template < > struct _higher_type<float,int> { typedef float type; };
 template < > struct _higher_type<float,long> { typedef float type; };
 template < > struct _higher_type<float,long long> { typedef float type; };
 template < > struct _higher_type<float,float> { typedef float type; };
 template < > struct _higher_type<float,double> { typedef double type; };
 template < > struct _higher_type<float,long double> { typedef long double type; };
 template < > struct _higher_type<double,int> { typedef double type; };
 template < > struct _higher_type<double,long> { typedef double type; };
 template < > struct _higher_type<double,long long> { typedef double type; };
 template < > struct _higher_type<double,float> { typedef double type; };
 template < > struct _higher_type<double,double> { typedef double type; };
 template < > struct _higher_type<double,long double> { typedef long double type; };
 template < > struct _higher_type<long double,int> { typedef long double type; };
 template < > struct _higher_type<long double,long> { typedef long double type; };
 template < > struct _higher_type<long double,long long> { typedef long double type; };
 template < > struct _higher_type<long double,float> { typedef long double type; };
 template < > struct _higher_type<long double,double> { typedef long double type; };
 template < > struct _higher_type<long double,long double> { typedef long double type; };
 template < typename T1, typename T2 >
 static inline typename _higher_type<T1,T2>::type
 _brian_mod(T1 x, T2 y)
 {{
     return x-y*floor(1.0*x/y);
 }}
 template < typename T1, typename T2 >
 static inline typename _higher_type<T1,T2>::type
 _brian_floordiv(T1 x, T2 y)
 {{
     return floor(1.0*x/y);
 }}
 #ifdef _MSC_VER
 #define _brian_pow(x, y) (pow((double)(x), (y)))
 #else
 #define _brian_pow(x, y) (pow((x), (y)))
 #endif

}

////// HASH DEFINES ///////



void _run_synapses_pre_codeobject()
{
	using namespace brian;


	///// CONSTANTS ///////////
	double* const _array_synapses_Apre = _dynamic_array_synapses_Apre.empty()? 0 : &_dynamic_array_synapses_Apre[0];
const int _numApre = _dynamic_array_synapses_Apre.size();
double* const _array_synapses_lastupdate = _dynamic_array_synapses_lastupdate.empty()? 0 : &_dynamic_array_synapses_lastupdate[0];
const int _numlastupdate = _dynamic_array_synapses_lastupdate.size();
int32_t* const _array_synapses__synaptic_pre = _dynamic_array_synapses__synaptic_pre.empty()? 0 : &_dynamic_array_synapses__synaptic_pre[0];
const int _num_synaptic_pre = _dynamic_array_synapses__synaptic_pre.size();
const int _numv = 100;
double* const _array_synapses_w = _dynamic_array_synapses_w.empty()? 0 : &_dynamic_array_synapses_w[0];
const int _numw = _dynamic_array_synapses_w.size();
const int _numt = 1;
double* const _array_synapses_Apost = _dynamic_array_synapses_Apost.empty()? 0 : &_dynamic_array_synapses_Apost[0];
const int _numApost = _dynamic_array_synapses_Apost.size();
const int _numnot_refractory = 100;
int32_t* const _array_synapses__synaptic_post = _dynamic_array_synapses__synaptic_post.empty()? 0 : &_dynamic_array_synapses__synaptic_post[0];
const int _num_postsynaptic_idx = _dynamic_array_synapses__synaptic_post.size();
	///// POINTERS ////////////
 	
 double* __restrict  _ptr_array_synapses_Apre = _array_synapses_Apre;
 double* __restrict  _ptr_array_synapses_lastupdate = _array_synapses_lastupdate;
 int32_t* __restrict  _ptr_array_synapses__synaptic_pre = _array_synapses__synaptic_pre;
 double* __restrict  _ptr_array_neurongroup_v = _array_neurongroup_v;
 double* __restrict  _ptr_array_synapses_w = _array_synapses_w;
 double*   _ptr_array_defaultclock_t = _array_defaultclock_t;
 double* __restrict  _ptr_array_synapses_Apost = _array_synapses_Apost;
 char* __restrict  _ptr_array_neurongroup_not_refractory = _array_neurongroup_not_refractory;
 int32_t* __restrict  _ptr_array_synapses__synaptic_post = _array_synapses__synaptic_post;



	// This is only needed for the _debugmsg function below	
	

	// scalar code
	const int _vectorisation_idx = -1;
 	
 const double t = _ptr_array_defaultclock_t[0];
 const double _lio_1 = 1.0f*1.0/0.005;
 const double _lio_2 = 1.0f*1.0/0.005;
 const double _lio_3 = (_brian_pow(0.01, 2)) * (_brian_pow(1.0, - 1));


	
	{
	std::vector<int> *_spiking_synapses = synapses_pre.peek();
	const unsigned int _num_spiking_synapses = _spiking_synapses->size();

	
	{
		for(unsigned int _spiking_synapse_idx=0;
			_spiking_synapse_idx<_num_spiking_synapses;
			_spiking_synapse_idx++)
		{
			const int _idx = (*_spiking_synapses)[_spiking_synapse_idx];
			const int _vectorisation_idx = _idx;
   			
   const int32_t _postsynaptic_idx = _ptr_array_synapses__synaptic_post[_idx];
   double Apre = _ptr_array_synapses_Apre[_idx];
   const char not_refractory = _ptr_array_neurongroup_not_refractory[_postsynaptic_idx];
   double lastupdate = _ptr_array_synapses_lastupdate[_idx];
   double v = _ptr_array_neurongroup_v[_postsynaptic_idx];
   double w = _ptr_array_synapses_w[_idx];
   double Apost = _ptr_array_synapses_Apost[_idx];
   const double _Apre = Apre * exp(_lio_1 * (- (t - lastupdate)));
   const double _Apost = Apost * exp(_lio_2 * (- (t - lastupdate)));
   Apre = _Apre;
   Apost = _Apost;
   if(not_refractory)
       v += _lio_3 * (w * v);
   Apre += 6.666666666666668e-06;
   w = _clip(w + Apost, 0, 0.0033333333333333335);
   lastupdate = t;
   _ptr_array_synapses_Apre[_idx] = Apre;
   _ptr_array_synapses_lastupdate[_idx] = lastupdate;
   _ptr_array_neurongroup_v[_postsynaptic_idx] = v;
   _ptr_array_synapses_w[_idx] = w;
   _ptr_array_synapses_Apost[_idx] = Apost;

		}
	}
    }

}

void _debugmsg_synapses_pre_codeobject()
{
	using namespace brian;
	std::cout << "Number of synapses: " << _dynamic_array_synapses__synaptic_pre.size() << endl;
}

