#include "objects.h"
#include "code_objects/synapses_synapses_create_array_codeobject_39.h"
#include "brianlib/common_math.h"
#include "brianlib/stdint_compat.h"
#include<cmath>
#include<ctime>
#include<iostream>
#include<fstream>
#include<climits>

////// SUPPORT CODE ///////
namespace {
 	
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



void _run_synapses_synapses_create_array_codeobject_39()
{
	using namespace brian;


	///// CONSTANTS ///////////
	int32_t* const _array_synapses__synaptic_post = _dynamic_array_synapses__synaptic_post.empty()? 0 : &_dynamic_array_synapses__synaptic_post[0];
const int _num_synaptic_post = _dynamic_array_synapses__synaptic_post.size();
const int _numN = 1;
int32_t* const _array_synapses__synaptic_pre = _dynamic_array_synapses__synaptic_pre.empty()? 0 : &_dynamic_array_synapses__synaptic_pre[0];
const int _num_synaptic_pre = _dynamic_array_synapses__synaptic_pre.size();
int32_t* const _array_synapses_N_incoming = _dynamic_array_synapses_N_incoming.empty()? 0 : &_dynamic_array_synapses_N_incoming[0];
const int _numN_incoming = _dynamic_array_synapses_N_incoming.size();
const int _numtargets = 15;
const int _numsources = 15;
int32_t* const _array_synapses_N_outgoing = _dynamic_array_synapses_N_outgoing.empty()? 0 : &_dynamic_array_synapses_N_outgoing[0];
const int _numN_outgoing = _dynamic_array_synapses_N_outgoing.size();
const int _num_postsynaptic_idx = _dynamic_array_synapses__synaptic_post.size();
const int _num_presynaptic_idx = _dynamic_array_synapses__synaptic_pre.size();
	///// POINTERS ////////////
 	
 int32_t* __restrict  _ptr_array_synapses__synaptic_post = _array_synapses__synaptic_post;
 int32_t*   _ptr_array_synapses_N = _array_synapses_N;
 int32_t* __restrict  _ptr_array_synapses__synaptic_pre = _array_synapses__synaptic_pre;
 int32_t* __restrict  _ptr_array_synapses_N_incoming = _array_synapses_N_incoming;
 int32_t* __restrict  _ptr_array_synapses_targets_39 = _array_synapses_targets_39;
 int32_t* __restrict  _ptr_array_synapses_sources_39 = _array_synapses_sources_39;
 int32_t* __restrict  _ptr_array_synapses_N_outgoing = _array_synapses_N_outgoing;



const int _old_num_synapses = _ptr_array_synapses_N[0];
const int _new_num_synapses = _old_num_synapses + _numsources;

const int _N_pre = 100;
const int _N_post = 100;
_dynamic_array_synapses_N_incoming.resize(_N_post + 0);
_dynamic_array_synapses_N_outgoing.resize(_N_pre + 0);

for (int _idx=0; _idx<_numsources; _idx++) {
        
    const int32_t sources = _ptr_array_synapses_sources_39[_idx];
    const int32_t targets = _ptr_array_synapses_targets_39[_idx];
    const int32_t _real_sources = sources;
    const int32_t _real_targets = targets;


    _dynamic_array_synapses__synaptic_pre.push_back(_real_sources);
    _dynamic_array_synapses__synaptic_post.push_back(_real_targets);
    // Update the number of total outgoing/incoming synapses per source/target neuron
    _dynamic_array_synapses_N_outgoing[_real_sources]++;
    _dynamic_array_synapses_N_incoming[_real_targets]++;
}

// now we need to resize all registered variables
const int newsize = _dynamic_array_synapses__synaptic_pre.size();
_dynamic_array_synapses__synaptic_post.resize(newsize);
_dynamic_array_synapses__synaptic_pre.resize(newsize);
_dynamic_array_synapses_Apost.resize(newsize);
_dynamic_array_synapses_Apre.resize(newsize);
_dynamic_array_synapses_delay.resize(newsize);
_dynamic_array_synapses_delay_1.resize(newsize);
_dynamic_array_synapses_lastupdate.resize(newsize);
_dynamic_array_synapses_w.resize(newsize);
// Also update the total number of synapses
_ptr_array_synapses_N[0] = newsize;


}


